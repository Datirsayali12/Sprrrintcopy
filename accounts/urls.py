from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView,CreatorRegistrationView,EmailVerificationView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('creator-register/', CreatorRegistrationView.as_view(), name='creator-register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changePassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('verify-email/<str:uidb64>/<str:token>/', EmailVerificationView.as_view(), name='email_verification'),

    ]