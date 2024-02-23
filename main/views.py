from django.shortcuts import render, redirect
from . import forms, models
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import Group
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login


def classroom_view(request):
    return render(request, 'classroom.html')

def home_view(request):
    context = {'user': request.user}
    return render(request, 'home.html', context)

def library_view(request):
    return render(request, 'library.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Перенаправляем пользователя на защищенную страницу
                return redirect('home')  # Укажите имя URL-маршрута для вашей защищенной страницы
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.contrib.auth.models import Group
from django.shortcuts import render, HttpResponseRedirect, reverse

def registration_view(request):
    if request.method == 'POST':
        userForm = forms.UserForm(request.POST)
        customForm = forms.CustomForm(request.POST, request.FILES)
        if userForm.is_valid() and customForm.is_valid():
            user = userForm.save(commit=False)
            password = userForm.cleaned_data['password']
            user.set_password(password)
            user.save()
            
            custom = customForm.save(commit=False)
            custom.user = user
            custom.save()
            
            # Add user to 'USER' group (create group if it doesn't exist)
            user_group, created = Group.objects.get_or_create(name='USER')
            user.groups.add(user_group)
            
            return HttpResponseRedirect(reverse('login'))
    else:
        userForm = forms.UserForm()
        customForm = forms.CustomForm()
        
    mydict = {'userForm': userForm, 'customForm': customForm}
    return render(request, 'registration.html', context=mydict)

