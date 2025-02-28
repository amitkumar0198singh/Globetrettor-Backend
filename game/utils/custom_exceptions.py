from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

class CustomException(Exception):
    message = None
    status_code = False
    detail = None

    def __init__(self, detail=None, status_code=None, message=None):
        self.detail = detail or self.detail
        self.status_code = status_code or self.status_code
        self.message = message or self.message


class DataNotFoundException(CustomException):
    message = "Data not found"
    status_code = status.HTTP_404_NOT_FOUND

class PasswordDoNotMatchException(CustomException):
    message = 'Password does not match'
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidCredentialException(CustomException):
    message = 'Invalid credential'
    status_code = status.HTTP_401_UNAUTHORIZED


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, CustomException):
        response = Response({'message': exc.message, 'status_code': exc.status_code,
                            'detail': exc.detail}, status=exc.status_code)
    return response