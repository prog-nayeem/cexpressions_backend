
from django.conf import settings
from .models import  User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from .helpers import Facebook, Google, register_social_user
from .exceptions import CustomAuthenticationFailed
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken 

ADMIN_EMAIL = settings.ADMIN_EMAIL
class UserRegisterSerializer(serializers.ModelSerializer):
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True,  error_messages={
            'min_length': 'Password must be at least 6 characters long.',
            'required': 'Please provide a password.',
        })

    class Meta:
        model=User
        fields = ['email', 'full_name', 'password', 'access_token', 'refresh_token']
        extra_kwargs = {
            'full_name': {'error_messages': {'required': 'Please provide your full name.'}},
        }

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Please provide a password.")
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value



    def create(self, validated_data):
        email = validated_data['email']
        full_name = validated_data.get('full_name')
        password = validated_data.get('password')
        is_admin = email == ADMIN_EMAIL 
    
        user = User.objects.create_user(
            email=email,
            full_name=full_name,
            password=password,
            is_staff=is_admin, 
            is_superuser=is_admin,
            is_verified=is_admin
        )
        
        tokens=user.tokens()
        return {
            'email': user.email,
            'full_name':user.full_name,
            "access_token":str(tokens.get('access')),
            "refresh_token":str(tokens.get('refresh'))
        }
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=155, error_messages= {'required': 'Please provide your email address.'})
    password=serializers.CharField(max_length=68, write_only=True, error_messages={
            'min_length': 'Password must be at least 6 characters long.',
            'required': 'Please provide a password.',
        })

    class Meta:
        model = User
        fields = ['email', 'password']
      
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request=self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise CustomAuthenticationFailed("Invalid credentials. Please try again.")
        
        tokens=user.tokens()
        return {
            'email':user.email,
            'full_name':user.full_name,
            "access_token":str(tokens.get('access')),
            "refresh_token":str(tokens.get('refresh'))
        }

class GoogleSignInSerializer(serializers.Serializer):
    access_token=serializers.CharField(min_length=6)


    def validate_access_token(self, access_token):
        if not access_token:
            raise serializers.ValidationError("Access token cannot be empty.")
        
        user_data=Google.validate(access_token)
        try:
            user_data['sub']
            
        except KeyError:
            raise serializers.ValidationError("Access token has expired or is invalid. Please try again.")
        
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
                raise AuthenticationFailed('Could not verify user.')

        user_id=user_data['sub']
        email=user_data['email']
        given_name = user_data.get('given_name', '')
        family_name = user_data.get('family_name', '')
        
        if given_name and family_name:
            full_name = f"{given_name} {family_name}"
        elif given_name:
            full_name = given_name
        elif family_name:
            full_name = family_name
        else:
            full_name = email.split('@')[0]


        provider='google'

        return register_social_user(provider, email, full_name)
    

class FacebookSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate_access_token(self, access_token):
        if not access_token:
            raise serializers.ValidationError("Access token cannot be empty.")
        
        user_data = Facebook.validate(access_token)
        try:
            user_data['id']
        except:
            raise serializers.ValidationError("Access token has expired or is invalid. Please try again.")

        full_name = user_data.get('name')
        if 'email' in user_data:
            email = user_data.get('email')
        else:
            email = f"{user_data.get('id')}@facebook.com"
            
        provider = 'facebook'

        return register_social_user(provider, email, full_name,)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    otp = serializers.CharField(min_length=6, max_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or OTP.")

        # Check OTP
        if not user.otp_code or user.otp_code != otp:
            raise serializers.ValidationError("Invalid OTP.")

        # Check Expiry
        if user.otp_created_at < timezone.now():
            user.otp_code = None
            user.otp_created_at = None
            user.save()
            raise serializers.ValidationError("OTP has expired.")
        
        # OTP is valid: Clear OTP fields
        user.otp_code = None
        user.otp_created_at = None
        
        # Generate a temporary, unique token 
        refresh = RefreshToken.for_user(user) 
        reset_token = str(refresh.access_token)
        
        user.reset_token = reset_token
        user.save()

        attrs['reset_token'] = reset_token
        return attrs

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, write_only=True)
    reset_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        reset_token = attrs.get('reset_token')

        try:
            user = User.objects.get(reset_token=reset_token)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired reset token.")
        
        # Clear the one-time token after successful validation
        user.reset_token = None
        user.save()

        attrs['user'] = user
        return attrs

    def save(self):
        password = self.validated_data['password']
        user = self.validated_data['user']
        user.set_password(password)
        user.save()
        return user
