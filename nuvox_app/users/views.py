from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm


class Login(auth_views.LoginView):

    template_name = 'admin/login.html'
    form_class = AuthenticationForm
    authentication_form = AuthenticationForm
