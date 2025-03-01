from datetime import datetime

from django.db.models import Q

from game.models.auth_model import User
from game.utils import custom_exceptions
from game.utils.tokens import get_tokens


def register_user(data: dict):
    user: User = User.objects.create_user(**data)
    token: dict = get_tokens(user)
    user.created_by = user
    user.updated_by = user
    user.save()
    data.pop('password')
    return {
        'status': True, 'message': "User registered successfully",
        'first_name': data.get('first_name'), 'last_name': data.get('last_name'),
        'username': data.get('username'), 'email': data.get('emai'), 'tokens': token
    }


def login_user(data):
    username_or_email = data.get('username_or_email')
    password = data.get('password')
    try:
        user: User = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
    except User.DoesNotExist:
        raise custom_exceptions.DataNotFoundException('User not found')
    if not user.check_password(password):
        raise custom_exceptions.InvalidCredentialException('Either username/email or password is wrong')
    token = get_tokens(user)
    return {
        'status': True, 'message': "User Logged in successfully",
        'first_name': user.first_name, 'last_name': user.last_name,
        'username': user.username, 'email': user.email, 'tokens': token
    }