from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import exception_handler

from rest_framework_simplejwt.exceptions import InvalidToken

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
    if isinstance(exc, InvalidToken):
        response = Response(
            {'message': 'Please provide valid token', "status_code": status.HTTP_403_FORBIDDEN,
             "status": False}, status=status.HTTP_401_UNAUTHORIZED)
    if isinstance(exc, NotAuthenticated):
        response = Response(
            {'message': 'Please provide token', "status_code": status.HTTP_403_FORBIDDEN,
             "status": False}, status=status.HTTP_403_FORBIDDEN)
    if isinstance(exc, CustomException):
        response = Response({'message': exc.message, 'status_code': exc.status_code,
                            'detail': exc.detail}, status=exc.status_code)
    elif response is not None:
        response.data['status_code'] = response.status_code
    else:
        response = Response(
            {'message': 'Something went wrong. Please try after some time',
             'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
             'detail': str(exc) if str(exc) else None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
