from django.shortcuts import render


def keyboard(request):
    return render(request=request, template_name='keyboard/keyboard.html')
