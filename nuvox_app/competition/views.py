from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView

from competition.models import Submission
from competition.forms import SubmissionForm


def competition(request):
    """Homepage for competition."""
    return render(request, template_name='competition/competition.html')


def submissions(request):
    """Submissions leaderboard."""
    all_submissions = Submission.objects.all()
    username_accuracy_tuples = [(submission.user.username, submission.top1_accuracy) for submission in all_submissions]
    ranked_username_accuracy_tuples = sorted(username_accuracy_tuples, key=lambda i: i[1], reverse=True)
    context = {
        'ranked_username_accuracy_tuples': ranked_username_accuracy_tuples
    }
    return render(request, template_name='competition/submissions.html', context=context)


class SubmissionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'competition/submit.html'
    success_url = reverse_lazy('submissions')
    success_message = 'Submission received successfully!'

    def form_valid(self, form):
        """ TODO Add missing fields to instance here."""
        form.instance.user = self.request.user
        return super(SubmissionCreateView, self).form_valid(form=form)
