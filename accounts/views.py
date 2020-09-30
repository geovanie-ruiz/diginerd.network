from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import FormView


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

class RegisterView(FormView):
    template_name = 'registration/sign_up.html'
