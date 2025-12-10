from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import serializers
from .exceptions import CustomAuthenticationFailed
from .serializers import FacebookSignInSerializer, GoogleSignInSerializer, UserRegisterSerializer, LoginSerializer, PasswordResetRequestSerializer, OTPVerificationSerializer, SetNewPasswordSerializer
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.conf import settings
from django.core.mail import send_mail
from smtplib import SMTPException
from .utils import generate_and_store_otp


User = get_user_model()


@method_decorator(ratelimit(key='ip', rate='10/m', method='POST'), name='post')
class RegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer=self.serializer_class(data=user_data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            formatted_errors = {}
            for field, errors in serializer.errors.items():
                formatted_errors[field] = errors[0]
            status_code = status.HTTP_400_BAD_REQUEST if 'email' in errors else status.HTTP_422_UNPROCESSABLE_ENTITY
            return Response({'errors': formatted_errors}, status=status_code)


@method_decorator(ratelimit(key='ip', rate='30/m', method='POST'), name='post')
class LoginUserView(GenericAPIView):
    serializer_class=LoginSerializer
    def post(self, request):
        serializer= self.serializer_class(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            formatted_errors = {}
            for field, errors in serializer.errors.items():
                formatted_errors[field] = errors[0]
            return Response({'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)
        except CustomAuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@method_decorator(ratelimit(key='ip', rate='30/m', method='POST'), name='post')
class GoogleOauthSignInview(GenericAPIView):
    serializer_class=GoogleSignInSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            
        except serializers.ValidationError:
            formatted_errors = {}
            for field, errors in serializer.errors.items():
                formatted_errors[field] = errors[0]
            status_code = status.HTTP_400_BAD_REQUEST if 'email' in errors else status.HTTP_422_UNPROCESSABLE_ENTITY
            return Response({'errors': formatted_errors}, status=status_code)
        except CustomAuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        data=((serializer.validated_data)['access_token'])
        return Response(data, status=status.HTTP_200_OK)


@method_decorator(ratelimit(key='ip', rate='30/m', method='POST'), name='post')
class FacebookOauthSignInView(GenericAPIView):
    serializer_class = FacebookSignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=((serializer.validated_data)['access_token'])
        return Response(data, status=status.HTTP_200_OK)


@method_decorator(ratelimit(key='ip', rate='20/m', method='POST'), name='post')
class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        otp_code = generate_and_store_otp(user) 

        try:
            send_mail(
                subject="Your Password Reset OTP",
                message=f"Your One-Time Password (OTP) for password reset is: {otp_code}. This code will expire in 5 minutes. Do not share this code.",                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False
            )
        except SMTPException as e:
        # Log the error for your own records
            print(f"Error sending email: {e}")
            return Response({"message": "Could not send OTP. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            

        return Response({"message": "Password reset OTP sent to your email."}, status=status.HTTP_200_OK)


@method_decorator(ratelimit(key='ip', rate='20/m', method='POST'), name='post')
class OTPVerifyView(GenericAPIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        reset_token = serializer.validated_data['reset_token']
        
        return Response({
            "message": "OTP verified successfully. Use the provided token to set your new password.",
            "reset_token": reset_token
        }, status=status.HTTP_200_OK)
    

@method_decorator(ratelimit(key='ip', rate='20/m', method='PATCH'), name='patch')
class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            # Format and return validation errors
            formatted_errors = {}
            for field, errors in serializer.errors.items():
                formatted_errors[field] = errors[0]
            return Response({'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)