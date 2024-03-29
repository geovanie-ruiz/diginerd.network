import requests
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email',
                             error_messages={'exists': 'Oops'})
    policy_agreement = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1',
                  'password2', 'policy_agreement')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(
                self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(*args, **kwargs)

    def post(self, form):
        request_body = self.request.POST
        if not request_body:
            return None

        # Begin reCAPTCHA validation #
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        ask_google = requests.post(url, data=data)
        result = ask_google.json()
        # End reCAPTCHA validation #

        if not result['success']:
            return redirect('login')
        return super().post(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
