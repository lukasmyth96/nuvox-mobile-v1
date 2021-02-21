import random
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django_user_agents.utils import get_user_agent
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from english_words import english_words_lower_alpha_set

from keyboard.apps import KeyboardConfig

@login_required()
def keyboard(request):
    context = {'is_mobile': request.user_agent.is_mobile}
    return render(request=request, template_name='keyboard/keyboard.html', context=context)

@login_required()
def predict(request):
    print('stop here')
    return JsonResponse({'predicted_words': ['test1', 'test2']})
