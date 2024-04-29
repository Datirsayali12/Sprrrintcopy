from rest_framework import serializers
from .models import User
from .models import Creator
from django.core.mail import send_mail
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


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
    profile_pic = serializers.URLField(write_only=True)
    terms_and_condition = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'confirm_password', 'profile_pic', 'terms_and_condition']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'error_messages': {'required': 'Email is required.'}},
            'name': {'error_messages': {'required': 'Name is required.'}},
            'confirm_password': {'error_messages': {'required': 'Confirm Password is required.'}},
            'profile_pic': {'error_messages': {'required': 'Profile Picture is required.'}},
            'terms_and_condition': {'error_messages': {'required': 'Terms and Condition agreement is required.'}}
        }

        def validate(self, attrs):
            required_fields = ['email', 'name', 'password', 'confirm_password', 'profile_pic', 'terms_and_condition']
            for field in required_fields:
                if field not in attrs:
                    error_message = {'messages': f"{field.capitalize()} required", 'status': "false"}
                    raise serializers.ValidationError(error_message)

            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            if password != confirm_password:
                raise serializers.ValidationError("Password and Confirm Password don't match")
            return attrs


def create(self, validated_data):
        profile_pic = validated_data.pop('profile_pic', None)
        terms_and_condition = validated_data.pop('terms_and_condition', False)
        validated_data.pop('confirm_password')

        user = User.objects.create_user(**validated_data)

        if profile_pic or terms_and_condition:
            creator_data = {'user': user}
            if profile_pic:
                creator_data['profile_pic'] = profile_pic
            if terms_and_condition:
                creator_data['terms_and_condition'] = terms_and_condition
            Creator.objects.create(**creator_data)

        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

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

        if not user.check_password(old_password):
            raise serializers.ValidationError("Incorrect old password")

        if old_password == new_password:
            raise serializers.ValidationError("New password must be different from the old password")

        user.set_password(new_password)
        user.save()
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
