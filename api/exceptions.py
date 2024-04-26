from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_detail = response.data.get('detail', None)
        if error_detail:
            response.data['error'] = error_detail
            del response.data['detail']
        else:
            response.data['error'] = 'Unknown error' 
        
        response.status_code = status.HTTP_400_BAD_REQUEST 

    return response
