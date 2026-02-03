from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=10000)

class Achivments(models.Model):
    game_name = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="achivments")
    name_achivments = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

class UserAchivment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userAchivments")
    achivment_id = models.ForeignKey(Achivments, on_delete=models.CASCADE, related_name="userAchivments")
    status = models.CharField(max_length=5)

class Order(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="orders")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    price = models.PositiveIntegerField()
