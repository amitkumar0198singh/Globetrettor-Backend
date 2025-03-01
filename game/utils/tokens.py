from game.models.player import Player

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens(player: Player) -> dict:
    refresh_token = RefreshToken.for_user(player)
    return {
        'access': str(refresh_token.access_token),
        'refresh': str(refresh_token) 
    }