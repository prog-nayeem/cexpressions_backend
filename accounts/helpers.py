import requests as rq
from google.auth.transport import requests
from google.oauth2 import id_token
from .models import User
from django.conf import settings
from .exceptions import CustomAuthenticationFailed


class Google():
    @staticmethod
    def validate(access_token):
        try:
            id_info=id_token.verify_oauth2_token(access_token, requests.Request())
            if 'accounts.google.com' in id_info['iss']:
                return id_info
        except Exception as e:
            print("token error: ", e)
            raise CustomAuthenticationFailed("The provided token is invalid or has expired. Please check and try again.")

class Facebook():
    @staticmethod
    def validate(access_token):
        try:
            fields = 'id,name,email,picture'
            response = rq.get('https://graph.facebook.com/me', params={'access_token': access_token, 'fields': fields})
            user_data = response.json()
            if 'id' in user_data:
                print("FB User Data: ", user_data)
                return user_data
        except Exception as e:
            print("Token error: ", e)
            return {}


def register_social_user(provider, email, full_name):
    try:
        user = User.objects.get(email=email)

        if user.auth_provider != provider:
            user.auth_provider = provider
            user.is_verified = True
            user.save()

        tokens = user.tokens()

        return {
            'email': user.email,
            'full_name': user.full_name,
            "access_token": str(tokens.get('access')),
            "refresh_token": str(tokens.get('refresh'))
        }

    except User.DoesNotExist:
        new_user = {
            'email': email,
            'full_name': full_name,
            'password': settings.SOCIAL_AUTH_PASSWORD
        }

        user = User.objects.create_user(**new_user)
        user.auth_provider = provider
        user.is_verified = True
        user.save()

        tokens = user.tokens()

        return {
            'email': user.email,
            'full_name': user.full_name,
            "access_token": str(tokens.get('access')),
            "refresh_token": str(tokens.get('refresh'))
        }
