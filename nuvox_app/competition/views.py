from django.shortcuts import render

from competition.models import Submission


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
