from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer,CreatorRegistrationSerializer
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes,  force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import AllowAny

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
    authentication_classes = []  # Exclude authentication for this view
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

      
            token = default_token_generator.make_token(user)

            current_site = get_current_site(request)
            domain = current_site.domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = f'http://{domain}{reverse("email_verification", kwargs={"uidb64": uid, "token": token})}'

            subject = 'Verify Your Email Address'
            message = f'Hi {user.name},\n\nPlease click the following link to verify your email address:\n{verification_url}'
            email = EmailMessage(subject, message, to=[user.email])
            email.send()

            return JsonResponse({'message': 'User registered successfully. Please check your email for verification instructions.','status':"true"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreatorRegistrationView(APIView):
    authentication_classes = []  # Exclude authentication for this view
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            serializer = CreatorRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                token = default_token_generator.make_token(user)

                current_site = get_current_site(request)
                domain = current_site.domain
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                verification_url = f'http://{domain}{reverse("email_verification", kwargs={"uidb64": uid, "token": token})}'

                subject = 'Verify Your Email Address'
                message = f'Hi {user.name},\n\nPlease click the following link to verify your email address:\n{verification_url}'
                email = EmailMessage(subject, message, to=[user.email])
                email.send()

                return JsonResponse({'message': 'User registered successfully. Please check your email for verification instructions.', 'status': "true"}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'message': 'Invalid data provided.', 'status': "false"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return JsonResponse({'message': 'Validation error occurred.', 'status': "false"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message': str(e), 'status': "false"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmailVerificationView(APIView):
    authentication_classes = []  # Exclude authentication for this view
    permission_classes = [AllowAny]
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            token = get_tokens_for_user(user)
            return JsonResponse({'token':token, 'message': 'Email verified successfully.','status':"true"}, status=status.HTTP_200_OK)
        return JsonResponse({'error': 'Invalid verification link.','status':'false'}, status=status.HTTP_400_BAD_REQUEST)
    



class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.email_verified:
                token = get_tokens_for_user(user)
                return JsonResponse({'token': token, 'message': 'Login Success','status':"true"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message': 'Email not verified. Please verify your email to log in.','status':'false'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse({'message': 'Email or Password is not Valid','status':'false'}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return JsonResponse({'data': serializer.data, 'status': 'true'}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]  # Assuming UserRenderer is defined elsewhere
  permission_classes = [IsAuthenticated]

  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
    serializer.is_valid(raise_exception=True)
    return JsonResponse({'message': 'Password Changed Successfully','status': 'true'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
  authentication_classes = []  # Exclude authentication for this view
  permission_classes = [AllowAny]
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return JsonResponse({'message':'Password Reset link send. Please check your Email','status': 'true'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  authentication_classes = []  # Exclude authentication for this view
  permission_classes = [AllowAny]
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return JsonResponse({'message':'Password Reset Successfully','status': 'true'}, status=status.HTTP_200_OK)








