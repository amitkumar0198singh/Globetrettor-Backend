from django.db import models

from game.models.base_model import BaseModel


class Destination(BaseModel):
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    clues = models.JSONField(null=True)
    fun_fact = models.JSONField(null=True)
    trivia = models.JSONField(null=True)


    class Meta:
        db_table = 'destination'


    def __str__(self):
        return f"{self.city}, {self.country}"