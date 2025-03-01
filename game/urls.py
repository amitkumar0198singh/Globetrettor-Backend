from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from game.views.auth_view import AuthView
from game.views.destination_view import DestinationView



router = DefaultRouter()
router.register(r'auth', AuthView, basename='auth')
router.register(r'destination', DestinationView, basename='destination')


urlpatterns = [
    path('', include(router.urls)),

    path('auth/token/refresh/', TokenRefreshView.as_view(), name='refresh_token')
]
