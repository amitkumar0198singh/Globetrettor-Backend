import random

from django.utils.timezone import now
from django.core.cache import cache

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from game.services import destination_service
from game.services import game_service


class GameView(viewsets.ViewSet):

    @action(detail=False, methods=['post'], url_path='start', url_name='start')
    def start_game(self, request):
        game_key = f'game_session_{request.user.id}'
        session_data = cache.get(game_key)
        if session_data:
            elapsed_time = (now() - session_data['start_time']).total_seconds()
            if elapsed_time >= 60:
                cache.delete(game_key)
        destination = random.choice(destination_service.get_all_destinations())
        choices = destination_service.get_destination_choices(destination.id)
        clues = destination.clues.split('\n')
        cache.set(game_key, {'destination_id': destination.id, 'start_time': now()}, timeout=60)
        return Response({'status': True, 'message': "Game Started!", 'clues': random.sample(clues, 2),
                        'choices': choices}, status=status.HTTP_200_OK)
    
    
    @action(detail=False, methods=['post'], url_path='guess', url_name='guess')
    def process_guess(self, request):
        user = request.user
        guessed_city = request.data.get('guess')
        if not guessed_city:
            return Response({"status": False, "message": "Please choose a city"}, 
                                                status=status.HTTP_400_BAD_REQUEST)
        game_key = f"game_session_{user.id}"
        session_data = cache.get(game_key)
        if not session_data:
            return Response({"status": False, "message": "No active game session. Start a new game!"}, 
                                                status=status.HTTP_400_BAD_REQUEST)
        guess_response = game_service.guess(guessed_city, session_data['destination_id'], user)
        return Response(guess_response, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'], url_path='score', url_name='score')
    def game_score(self, request):
        score_key = f'player_score_{request.user.id}'
        score = cache.get(score_key, {'correct': 0, 'incorrect': 0})
        return Response({'status': True, 'message': "Score fetched", 'score': score}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'], url_path='end', url_name='end')
    def end_game(self, request):
        game_response = game_service.end(request.user)
        return Response(game_response, status=status.HTTP_200_OK if game_response.get('status') \
                        else status.HTTP_400_BAD_REQUEST)