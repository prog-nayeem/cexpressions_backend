from django.urls import path
from .views import (
        FacebookOauthSignInView,
        GoogleOauthSignInview,
        RegisterView,
        LoginUserView, 
         )

from rest_framework_simplejwt.views import (TokenRefreshView,)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginUserView.as_view(), name='login-user'),
    path('google/', GoogleOauthSignInview.as_view(), name='google_login'),
    path('facebook/', FacebookOauthSignInView.as_view(), name='facebook_login')
    ]