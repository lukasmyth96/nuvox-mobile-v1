from django.shortcuts import render


def keyboard(request):
    context = {'is_mobile': request.user_agent.is_mobile}
    return render(request=request, template_name='keyboard/keyboard.html', context=context)
