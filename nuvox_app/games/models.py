from datetime import datetime

from django.db import models

from users.models import User


class Game(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    @property
    def has_expired(self) -> bool:
        """Returns True if game was created over 60s ago."""
        return (datetime.now(tz=self.created_on.tzinfo) - self.created_on).total_seconds() > 10
