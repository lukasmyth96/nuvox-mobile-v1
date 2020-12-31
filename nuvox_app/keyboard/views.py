import random
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django_user_agents.utils import get_user_agent
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from wordfreq import top_n_list

from keyboard.models import DataCollectionSwipe, DeviceType
from keyboard.serializers import DataCollectionSwipeSerializer
from keyboard.validators import trace_matches_target_text


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
        """Add additional fields to serializer before saving."""
        user_agent = get_user_agent(self.request)
        if user_agent.is_mobile:
            device_type = DeviceType.MOBILE
        elif user_agent.is_tablet:
            device_type = DeviceType.TABLET
        elif user_agent.is_pc:
            device_type = DeviceType.PC
        else:
            device_type = DeviceType.OTHER
        trace_matches_text = trace_matches_target_text(
            trace=serializer.validated_data['trace'],
            target_text=serializer.validated_data['target_text']
        )
        serializer.save(
            user=self.request.user,
            trace_matches_text=trace_matches_text,
            device_type=device_type
        )
