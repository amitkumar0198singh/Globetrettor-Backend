from rest_framework import serializers

from game.utils import custom_exceptions
from game.models.auth_model import User

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']
        required = ['email', 'password', 'confirm_password']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise custom_exceptions.PasswordDoNotMatchException('Passowrd and Confirm Password do not match')
        return data
    

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    