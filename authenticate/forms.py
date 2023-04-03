from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Nom d’utilisateur')

    password = forms.CharField(
        max_length=63,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
        label='Mot de passe')


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({'class': 'form-control'})
        self.fields["email"].widget.attrs.update({'class': 'form-control'})
        self.fields["password1"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields["password2"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
