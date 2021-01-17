from django import forms

from competition.models import Submission


class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission

        fields = [
            'description',
            'predictions'
        ]
