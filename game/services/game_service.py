import random

from django.core.cache import cache

from game.models.profile import Profile
from game.services import destination_service


def guess(guessed_city, destination_id, player):
    destination = destination_service.get_destination(destination_id)
    correct = guessed_city.lower() == destination.city.lower()
    fun_fact = destination.fun_fact.split('\n')

    cache_key = f'player_score_{player.id}'
    score = cache.get(cache_key, {'correct': 0, 'incorrect': 0})
    if correct:
        score['correct'] += 1
    else:
        score['incorrect'] += 1
    cache.set(cache_key, score)
    player_profile, created = Profile.objects.get_or_create(player=player)
    player_profile.latest_score = score['correct']
    if score['correct'] > player_profile.highest_score:
        player_profile.highest_score = score['correct']
    player_profile.save()
    return {
        "correct": correct,
        "message": "🎉 Correct! Here's a fun fact:" if correct else "😢 Incorrect! But did you know?",
        "fun_fact": random.choice(fun_fact),
        "updated_score": score
    }


def end(player):
    game_key = f'game_session_{player.id}'
    score_key = f'player_score_{player.id}'
    if not cache.get(game_key):
        return {'status': False, 'message': "No active game session!"}
    score = cache.get(score_key, {'correct': 0, 'incorrect': 0})
    cache.delete(game_key)
    cache.delete(score_key)
    return {'status': True, 'message': "Game over!", 'final_score': score}