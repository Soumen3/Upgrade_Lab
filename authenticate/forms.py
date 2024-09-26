from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


tailwindcss = 'dark:bg-gray-700 dark:text-white'

class RegisterForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': tailwindcss}),
            'email': forms.EmailInput(attrs={'class': tailwindcss}),
            'first_name': forms.TextInput(attrs={'class': tailwindcss}),
            'last_name': forms.TextInput(attrs={'class': tailwindcss}),
            'password1': forms.PasswordInput(attrs={'class': tailwindcss}),
            'password2': forms.PasswordInput(attrs={'class': tailwindcss}),
        }

class LoginForm(AuthenticationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': tailwindcss}),
            'password': forms.PasswordInput(attrs={'class': tailwindcss}),
        }