from django.db import models

# Create your models here.


class Player(models.Model):
    name = models.CharField(max_length=100, default='name')
    points = models.IntegerField(default=0)

class Match(models.Model):
    team1 = models.CharField(max_length=100, default=None)
    team2 = models.CharField(max_length=100, default=None)
    team1_goals = models.IntegerField(default=0)
    team2_goals = models.IntegerField(default=0)
    date = models.DateField(default=None)
    time = models.TimeField(default=None)

