from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import UserManager
import os
AUTH_PROVIDERS ={'email':'email', 'google':'google', 'facebook':'facebook'}

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, editable=False) 
    email = models.EmailField(
        max_length=255, verbose_name=_("Email Address"), unique=True, error_messages= {'required': 'Please provide your email address.', 'unique': 'A user with this email address already exists.'}
    )
    full_name = models.CharField(max_length=100, verbose_name=_("Full Name"), error_messages= {'required': 'Please provide your full name.'})
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    auth_provider=models.CharField(max_length=50, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def tokens(self):    
        refresh = RefreshToken.for_user(self)
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

