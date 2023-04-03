from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from . import forms
from BigDataProject import settings

# Create your views here.


class SigninPageView(View):
    template_name = 'signin.html'
    form_class = forms.SignInForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})


class SignupPageView(View):
    template_name = 'signup.html'
    form_class = forms.SignUpForm

    def get(self, request):
        form = self.form_class()
        print(form)
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})


def signout_user(request):
    logout(request)
    return redirect('signin')
