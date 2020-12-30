import random
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from wordfreq import top_n_list


def keyboard(request):
    context = {'is_mobile': request.user_agent.is_mobile}
    return render(request=request, template_name='keyboard/keyboard.html', context=context)


@require_http_methods(['GET'])
def random_word(request):
    word_list = top_n_list('en', 1000)
    word = random.choice(word_list)
    return JsonResponse({'word': word})
