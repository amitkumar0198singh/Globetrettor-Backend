from django.db.models import Q

from game.models.player import Player
from game.utils import custom_exceptions



def get_player_by_id(id):
    try:
        return Player.objects.get(id=id)
    except Player.DoesNotExist:
        raise custom_exceptions.DataNotFoundException('Player not found')

def get_player_by_username(username):
    try:
        return Player.objects.get(username=username)
    except Player.DoesNotExist:
        raise custom_exceptions.DataNotFoundException('Player not found')


def get_player_by_email(email):
    try:
        return Player.objects.get(email=email)
    except Player.DoesNotExist:
        raise custom_exceptions.DataNotFoundException('Player not found')
    

def get_player_by_username_or_email(username_or_email):
    try:
        return Player.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
    except Player.DoesNotExist:
        raise custom_exceptions.DataNotFoundException('Player not found')
    

def get_player(field_name, field_value):
    try:
        return Player.objects.get(**{field_name: field_value})
    except Player.DoesNotExist:
        raise custom_exceptions.DataNotFoundException('Player not found')
    


def invite_player(invited_player_username, invited_by):
    player: Player = Player.objects.create_player(username=invited_player_username, is_invited=True)
    player.is_invited = True
    player.invited_by = invited_by
    player.created_by = invited_by
    player.updated_by = invited_by
    player.save()
    return {
        'status': True, 'message': "Player Invited successfully", 'player': invited_player_username 
    }