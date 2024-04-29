from urllib import request

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User
from .models import Creator
from django.core.mail import send_mail
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import os
from django.conf import settings
import uuid


# from .utils import send_mail_to_client

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'confirm_password', 'is_customer']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm Password don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password from data
        return User.objects.create_user(**validated_data)


class CreatorRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    profile_pic = serializers.ImageField(write_only=True)
    terms_and_condition = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'confirm_password', 'profile_pic', 'terms_and_condition']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'error_messages': {'required': 'Email is required.'}},
            'name': {'error_messages': {'required': 'Name is required.'}},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')  # Remove confirm_password from attrs
        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm Password don't match")

        # Validate password strength using Django's built-in password validation
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        # Validate terms_and_condition
        if not attrs.get('terms_and_condition'):
            raise serializers.ValidationError("Terms and Conditions agreement is required.")

        return attrs

    def create(self, validated_data):
        profile_pic = validated_data.pop('profile_pic')  # Extracting profile pic data
        terms_and_condition = validated_data.pop('terms_and_condition', False)  # Extracting terms_and_condition

        # Create user object
        user = User.objects.create_user(**validated_data)

        # Process profile pic and store it with a unique URL
        file_name = generate_unique_filename(profile_pic.name)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb+') as destination:
            for chunk in profile_pic.chunks():
                destination.write(chunk)
        file_url = settings.MEDIA_URL + file_name

        # Create creator object and associate with the user
        creator = Creator.objects.create(user=user, profile_pic=file_url, terms_and_condition=terms_and_condition)

        return user
def generate_unique_filename(filename):
    # Generate a unique filename using uuid
    unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[-1]
    return unique_filename

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, error_messages={'required': 'Email is required.',
                                                                   'invalid': 'Enter a valid email address.'})
    password = serializers.CharField(error_messages={'required': 'Password is required.'})

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        user = self.context.get('user')
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')

        if not old_password:
            raise serializers.ValidationError("Old password cannot be blank")
        if not new_password:
            raise serializers.ValidationError("New password cannot be blank")

        if not user.check_password(old_password):
            raise serializers.ValidationError("Incorrect old password")

        if old_password == new_password:
            raise serializers.ValidationError("New password must be different from the old password")

        # Validate the strength of the new password
        try:
            validate_password(new_password, user=user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return attrs



def send_mail_to_client(subject, body, to_email):
    send_mail(subject, body, None, [to_email])


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/api/user/reset/' + uid + '/' + token
            body = 'Click the following link to reset your password: ' + link
            subject = 'Reset Your Password'

            # Call send_mail_to_client method to send the email
            send_mail_to_client(subject, body, user.email)

            return attrs
        else:
            raise serializers.ValidationError('You are not a registered user')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != confirm_password:
                raise serializers.ValidationError("Password and Confirm Password don't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
