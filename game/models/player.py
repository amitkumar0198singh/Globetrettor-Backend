from django.db import models
from game.models.base_model import BaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class PlayerManager(BaseUserManager):
    def create_player(self, username, email=None, password=None, first_name=None,
                                                last_name=None, is_invited=False):
        if not username:
            raise ValueError('Player must have a username')
        if not is_invited and not email:
            raise ValueError('Email is required for regular players')
        player = self.model(
            username=username,
            email=self.normalize_email(email) if email else None,
            first_name=first_name,
            last_name=last_name
        )
        if not password:
            player.set_unusable_password()
        else:
            player.set_password(password)
        player.save(using=self._db)
        return player


class Player(BaseModel, AbstractBaseUser):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_invited = models.BooleanField(default=False)
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, db_column='invited_by')
    password_updated_at = models.DateTimeField(auto_now_add=True)
    last_login = None
    
    objects = PlayerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username or self.email 
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'player'