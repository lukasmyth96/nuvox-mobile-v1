import random
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from wordfreq import top_n_list

from keyboard.models import DataCollectionSwipe
from keyboard.serializers import DataCollectionSwipeSerializer


@login_required()
def keyboard(request):
    context = {'is_mobile': request.user_agent.is_mobile}
    return render(request=request, template_name='keyboard/keyboard.html', context=context)


@require_http_methods(['GET'])
def random_word(request):
    word_list = top_n_list('en', 1000)
    word = random.choice(word_list)
    return JsonResponse({'word': word})


class CollectedSessionViewSet(viewsets.ModelViewSet):
    queryset = DataCollectionSwipe.objects.all()
    serializer_class = DataCollectionSwipeSerializer
    http_method_names = ['post']
    # permission_classes = [IsAuthenticated]  # TODO uncomment after testing

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
