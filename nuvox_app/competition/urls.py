from django.urls import path, include

from competition.views import competition

urlpatterns = [
    path('competition/', competition, name='competition'),
    ]
