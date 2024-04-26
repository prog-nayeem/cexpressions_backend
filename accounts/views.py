from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import serializers
from .exceptions import CustomAuthenticationFailed
from .serializers import FacebookSignInSerializer, GoogleSignInSerializer, UserRegisterSerializer, LoginSerializer
from rest_framework import status

# Create your views here.

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

        
class FacebookOauthSignInView(GenericAPIView):
    serializer_class = FacebookSignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=((serializer.validated_data)['access_token'])
        return Response(data, status=status.HTTP_200_OK)