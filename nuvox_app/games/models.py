from django.db import models

from users.models import User


class Game(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
