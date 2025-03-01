from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from game.services import auth_service
from game.serializers.auth_serializer import LoginSerializer, RegistrationSerializer


class AuthView(viewsets.ViewSet):

    @action(detail=False, methods=['post'], url_path='registration', url_name='registration')
    def user_registration(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = auth_service.register_user(serializer.validated_data)
        return Response(response, status=status.HTTP_201_CREATED)
    

    @action(detail=False, methods=['post'], url_path='login', url_name='login')
    def user_login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = auth_service.login_user(serializer.validated_data)
        return Response(response, status=status.HTTP_200_OK)