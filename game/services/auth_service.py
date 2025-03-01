from datetime import datetime

from django.db.models import Q

from game.models.player import Player
from game.services import player_service
from game.utils import custom_exceptions
from game.utils.tokens import get_tokens


def register_player(data: dict):
    user: Player = Player.objects.create_player(**data)
    token: dict = get_tokens(user)
    user.created_by = user
    user.updated_by = user
    user.save()
    data.pop('password')
    return {
        'status': True, 'message': "Player registered successfully", 'player': data, 'tokens': token
    }


def login_player(data):
    username_or_email = data.get('username_or_email')
    password = data.get('password')
    player : Player = player_service.get_player_by_username_or_email(username_or_email)
    if not player.is_invited and not player.check_password(password):
        raise custom_exceptions.InvalidCredentialException('Either username/email or password is wrong')
    token = get_tokens(player)
    return {
        'status': True, 'message': "Player Logged in successfully",
        'first_name': player.first_name, 'last_name': player.last_name,
        'username': player.username, 'email': player.email, 'tokens': token
    }