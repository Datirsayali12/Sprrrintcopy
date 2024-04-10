from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView,CreatorRegistrationView,EmailVerificationView


class TokenRefreshAPIView(TokenRefreshView):
    pass  # This view will handle token refresh, no need to implement anything


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('creator-register/', CreatorRegistrationView.as_view(), name='creator-register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changePassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('verify-email/<str:uidb64>/<str:token>/', EmailVerificationView.as_view(), name='email_verification'),
    path('api/token/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)