import random

from django.core.cache import cache

from game.models.leaderboard import Leaderboard
from game.services import destination_service


def guess(guessed_city, destination_id, player):
    destination = destination_service.get_destination(destination_id)
    correct = guessed_city.lower() == destination.city.lower()
    fun_fact = destination.fun_fact.split('\n')

    leaderboard_entry, created = Leaderboard.objects.get_or_create(player=player)
    if correct:
        leaderboard_entry.correct_answer += 1
    else:
        leaderboard_entry.incorrect_answer += 1
    leaderboard_entry.save()
    score = {'correct': leaderboard_entry.correct_answer, 'incorrect': leaderboard_entry.incorrect_answer}
    return {
        "correct": correct,
        "message": "🎉 Correct! Here's a fun fact:" if correct else "😢 Incorrect! But did you know?",
        "fun_fact": random.choice(fun_fact),
        "updated_score": score
    }


def end(player):
    game_key = f'game_session_{player.id}'
    score_key = f'user_score_{player.id}'
    if not cache.get(game_key):
        return {'status': False, 'message': "No active game session!"}
    score = cache.get(score_key, {'correct': 0, 'incorrect': 0})
    cache.delete(game_key)
    cache.delete(score_key)
    leaderboard_entry, created = Leaderboard.objects.get_or_create(player=player)
    if score['correct'] > leaderboard_entry.correct_answer:
        leaderboard_entry.correct_answer = score['correct']
        leaderboard_entry.incorrect_answer = score['incorrect']
        leaderboard_entry.save()
    return {'status': True, 'message': "Game over!", 'final_score': score}