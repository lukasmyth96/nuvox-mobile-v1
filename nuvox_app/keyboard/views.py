import random

from english_words import english_words_set
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


def keyboard(request):
    context = {'is_mobile': request.user_agent.is_mobile}
    return render(request=request, template_name='keyboard/keyboard.html', context=context)


@require_http_methods(['GET'])
def random_word(request):
    english_words_list = list(english_words_set)
    word = random.choice(english_words_list)
    return JsonResponse({'word': word})
