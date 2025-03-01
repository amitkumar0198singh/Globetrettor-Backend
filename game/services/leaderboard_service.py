from game.models.leaderboard import Leaderboard
from game.utils import custom_exceptions


def get_player(player):
    try:
        return Leaderboard.objects.get(player=player)
    except Leaderboard.DoesNotExist:
        raise custom_exceptions.DataNotFoundException('Please start a game')

def get_leaderboard():
    return Leaderboard.objects.all().order_by('-correct_answer')[:10]