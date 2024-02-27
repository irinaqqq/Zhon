from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']  # Include 'username' and 'email' from default User model
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Құпия сөз'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Аты'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Тегі'}),
            'username': forms.TextInput(attrs={'placeholder': 'Пайдаланушы аты'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Электрондық пошта'}),
        }

class CustomForm(forms.ModelForm):
    class Meta:
        model = Custom
        fields = ['profile_pic']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'placeholder': 'Профиль суреті'}),
        }

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'description']