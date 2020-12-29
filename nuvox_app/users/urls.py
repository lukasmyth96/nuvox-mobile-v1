from django.urls import path

from .views import LoginView, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    ]
