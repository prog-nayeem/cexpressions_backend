import requests as rq
from google.auth.transport import requests
from google.oauth2 import id_token
from .models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
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
    old_user=User.objects.filter(email=email)
    if old_user.exists():
        if provider == old_user[0].auth_provider:
            register_user=authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)
            tokens = register_user.tokens()
            
            return {
                'full_name':register_user.full_name,
                'email':register_user.email,
                'access_token':str(tokens.get('access')),
                'refresh_token': str(tokens.get('refresh'))
            }
        else:
            raise CustomAuthenticationFailed(f"Please continue your login with {old_user[0].auth_provider}")
    else:
        new_user={
            'email':email,
            'full_name':full_name,
            'password':settings.SOCIAL_AUTH_PASSWORD
        }

        user=User.objects.create_user(**new_user)
        user.auth_provider=provider
        user.is_verified=True
        user.save()
        login_user=authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)
        tokens=login_user.tokens()
        
        return {
            'email':login_user.email,
            'full_name':login_user.full_name,
            "access_token":str(tokens.get('access')),
            "refresh_token":str(tokens.get('refresh'))
        }
