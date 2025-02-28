from django.db import models
from game.models.base_model import BaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name=None, last_name=None, username=None):
        if not email:
            raise ValueError('User must have an email id')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(BaseModel, AbstractBaseUser):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, unique=True, null=True)
    email = models.CharField(max_length=255, unique=True, null=True)
    # password = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    password_updated_at = models.DateTimeField(auto_now_add=True)
    last_login = None
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username or self.email 
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'user'