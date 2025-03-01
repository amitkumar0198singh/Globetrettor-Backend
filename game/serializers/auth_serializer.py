from rest_framework import serializers

from game.services import player_service
from game.utils import custom_exceptions
from game.models.player import Player

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']
        required = ['email', 'password', 'confirm_password']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise custom_exceptions.PasswordDoNotMatchException('Passowrd and Confirm Password do not match')
        return data
    

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        player: Player = player_service.get_player('username', data.get('username_or_email'))
        if not player.is_invited and not data.get('password'):
            raise custom_exceptions.PasswordRequiredException('Password is required for regular players')
        return data
            