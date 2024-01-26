from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import UserProfile
from django.forms.widgets import PasswordInput, TextInput

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())