from django.db import models

from users.models import User
from keyboard.validators import validate_trace


class BaseSwipe(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    trace = models.JSONField(validators=[validate_trace])
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """Overriding to validate the trace before saving."""
        validate_trace(trace=self.trace)
        super(BaseSwipe, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )


class DataCollectionSwipe(BaseSwipe):
    target_text = models.CharField(max_length=255)
    trace_matches_text = models.BooleanField()  # is trace sufficiently accurate.

    def __str__(self):
        return f'target_text: {self.target_text} - trace_matches_text: {self.trace_matches_text}'
