from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from competition.validators import validate_submission_predictions


class Submission(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='submissions')
    description = models.TextField(null=True, blank=True)
    predictions = models.JSONField(validators=[validate_submission_predictions])
    top1_accuracy = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    top3_accuracy = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """Overriding to validate the predictions before saving."""
        validate_submission_predictions(predictions=self.predictions)
        super(Submission, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
