from django.shortcuts import render


def competition(request):
    return render(request, template_name='competition/competition.html')

