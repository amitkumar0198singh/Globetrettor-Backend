from django.db import models

from game.models.base_model import BaseModel
from game.models.player import Player


class Profile(BaseModel):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, db_column='player',
                                                                related_name='profile')
    latest_score = models.IntegerField(default=0)
    highest_score = models.IntegerField(default=0)


    class Meta:
        db_table = 'profile'