from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import SignUpForm


class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    authentication_form = AuthenticationForm


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')
    form_class = SignUpForm
    success_message = "Your account was created successfully"
