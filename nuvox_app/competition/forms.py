from django import forms

from competition.models import Submission


class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission

        fields = [
            'description',
            'predictions'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

        help_texts = {
            'description': 'Give a description of your algorithm...',
            'predictions': 'Copy and paste the contents of submission.json here...'
        }
