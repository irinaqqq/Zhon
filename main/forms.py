from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']  
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
        fields = ['name',]

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description', 'classroom', 'images'] 

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['classroom'].queryset = Classroom.objects.all()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['classroom', 'topic', 'question', 'question_type', 'choice1', 'choice2', 'choice3', 'choice4', 'correct_answer']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.all()  

 
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'placeholder': 'Профиль суреті'}),
        }