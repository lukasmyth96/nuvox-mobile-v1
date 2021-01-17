from django.urls import path, include

from competition.views import competition, submissions, SubmissionCreateView

urlpatterns = [
    path('competition/', competition, name='competition'),
    path('competition/submissions/', submissions, name='submissions'),
    path('competition/submit/', SubmissionCreateView.as_view(), name='submit'),
]
