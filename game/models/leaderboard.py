from django.db import models

from game.models.auth_model import User

class Leaderboard(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.OneToOneField(User, on_delete=models.CASCADE, 
                                db_column='player', related_name='leaderboard')
    correct_answer = models.IntegerField(default=0)
    incorrect_answer = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} -- {self.correct_answer} correct"
    
    class Meta:
        db_table = 'leaderboard'