from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.contrib.humanize.templatetags.humanize import ordinal

from competition.models import Submission
from competition.forms import SubmissionForm
from competition.utils import evaluate_submission


def competition(request):
    """Homepage for competition."""
    return render(request, template_name='competition/competition.html')


def submissions(request):
    """Submissions leaderboard."""
    all_submissions = Submission.objects.all()

    username_accuracy_tuples = [(submission.user.username, submission.top1_accuracy) for submission in all_submissions]
    ranked_username_accuracy_tuples = sorted(username_accuracy_tuples, key=lambda i: i[1], reverse=True)
    users_best_score = None
    users_best_rank = None
    for idx, (username, score) in enumerate(ranked_username_accuracy_tuples):
        if username == request.user.username:
            users_best_rank = idx + 1
            users_best_score = f'{score:.1%}'
    context = {
        'ranked_username_accuracy_tuples': [(username, f'{score:.1%}') for username, score in ranked_username_accuracy_tuples],
        'users_best_rank': ordinal(users_best_rank),
        'users_best_score': users_best_score
    }
    return render(request, template_name='competition/submissions.html', context=context)


class SubmissionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'competition/submit.html'
    success_url = reverse_lazy('submissions')
    success_message = 'Submission received successfully!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        top1_acc, top3_acc = evaluate_submission(predictions=form.instance.predictions)
        form.instance.top1_accuracy = top1_acc
        form.instance.top3_accuracy = top3_acc
        return super(SubmissionCreateView, self).form_valid(form=form)
