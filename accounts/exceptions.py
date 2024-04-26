from rest_framework import exceptions

class CustomAuthenticationFailed(exceptions.APIException):
    status_code = 401
    default_detail = 'Invalid credentials provided.'
    default_code = 'authentication_failed'
