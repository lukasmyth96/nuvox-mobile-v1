from django.urls import path, include

from competition.views import competition, submissions

urlpatterns = [
    path('competition/', competition, name='competition'),
    path('submissions/', submissions, name='submissions')
]
