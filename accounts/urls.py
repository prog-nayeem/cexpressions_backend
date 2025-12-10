from django.urls import path
from .views import (
        FacebookOauthSignInView,
        GoogleOauthSignInview,
        RegisterView,
        LoginUserView, 
        PasswordResetRequestView,
        OTPVerifyView,
        SetNewPasswordView
         )

from rest_framework_simplejwt.views import (TokenRefreshView,)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginUserView.as_view(), name='login-user'),
    path('google/', GoogleOauthSignInview.as_view(), name='google_login'),
    path('facebook/', FacebookOauthSignInView.as_view(), name='facebook_login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('verify-otp/', OTPVerifyView.as_view(), name='password-reset-verify'),
    path('password-reset-confirm/', SetNewPasswordView.as_view(), name='password-reset-confirm'),
    ]