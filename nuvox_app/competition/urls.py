from django.urls import path, include

from competition.views import competition, submissions

urlpatterns = [
    path('competition/', competition, name='competition'),
    path('competition/submissions/', submissions, name='submissions')
]
