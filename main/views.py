from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import Group
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.db.models import Count
from datetime import datetime, timedelta
from .models import *
from .forms import *
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
        userForm = UserForm(request.POST)
        customForm = CustomForm(request.POST, request.FILES)
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
        userForm = UserForm()
        customForm = CustomForm()
        
    mydict = {'userForm': userForm, 'customForm': customForm}
    return render(request, 'registration.html', context=mydict)

def profile_view(request):
    # Get the user's profile information
    profile_info = Custom.objects.get(user=request.user)
    
    # Define start and end dates (for example, for the current month)
    start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date.replace(day=1, month=start_date.month+1) - timedelta(days=1)
    
    # Query and count tasks completed by the user within the date range
    tasks_count_by_date = get_tasks_count_by_date(request.user, start_date, end_date)
    
    # Render the profile page template with the profile information and tasks count data
    return render(request, 'profile.html', {'profile_info': profile_info, 'tasks_count_by_date': tasks_count_by_date})

def get_tasks_count_by_date(user, start_date, end_date):
    tasks_count_by_date = Task.objects.filter(
        user=user,
        completed=True,
        completion_date__range=[start_date, end_date]
    ).values('completion_date').annotate(count=Count('id'))

    return tasks_count_by_date

def admin_panel(request):
    classrooms = Classroom.objects.all()
    if request.method == 'POST':
        if 'create_class' in request.POST:
            form = ClassroomForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin_panel')
    else:
        form = ClassroomForm()
    return render(request, 'admin_panel.html', {'classrooms': classrooms, 'form': form})


def edit_class(request, class_id):
    classroom = get_object_or_404(Classroom, pk=class_id)
    if request.method == 'POST':
        if 'delete_class' in request.POST:
            classroom.delete()
            return redirect('admin_panel')
        else:
            form = ClassroomForm(request.POST, instance=classroom)
            if form.is_valid():
                form.save()
                return redirect('admin_panel')
    else:
        form = ClassroomForm(instance=classroom)
    return render(request, 'edit_class.html', {'form': form})