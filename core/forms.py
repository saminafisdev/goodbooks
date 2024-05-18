from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from core.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
