from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from game.services import player_service



class InvitePlayerView(APIView):
    def post(self, request):
        player_username = request.data.get('player_username')
        if not player_username:
            return Response({"status": False, "message": "Please create a username"},
                                                        status=status.HTTP_400_BAD_REQUEST)
        response = player_service.invite_player(player_username, request.user)
        return Response(response, status=status.HTTP_201_CREATED)
    

class LeaderbaordView(APIView):
   def get(self, request):
        leaderboard = player_service.get_player_leaderboard()
        leaderboard_list = [{'username': lb.player.username, 'highest_score': lb.highest_score} for lb in leaderboard]
        return Response(leaderboard_list, status=status.HTTP_200_OK)