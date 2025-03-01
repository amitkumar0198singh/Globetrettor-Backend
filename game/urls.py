from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from game.views.auth_view import AuthView
from game.views.destination_view import DestinationView
from game.views.game_view import GameView
from game.views.player_view import InvitePlayerView
from game.views.player_view import LeaderbaordView


router = DefaultRouter()
router.register(r'player/auth', AuthView, basename='auth')
router.register(r'destination', DestinationView, basename='destination')
router.register(r'game', GameView, basename='game')

urlpatterns = [
    path('', include(router.urls)),
    path('player/invite-player/', InvitePlayerView.as_view(), name='invite_player'),
    path('player/leaderboard/',  LeaderbaordView.as_view(), name='leaderboard'),
    path('player/auth/token/refresh/', TokenRefreshView.as_view(), name='refresh_token')
]
