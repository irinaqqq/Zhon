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
from django.contrib.admin.views.decorators import staff_member_required

def classroom_view(request):
    classrooms = Classroom.objects.order_by('name')
    return render(request, 'classroom.html', {'classrooms': classrooms})

def classroom_topics(request, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    topics = classroom.topic_set.all()
    return render(request, 'classroom_topics.html', {'classroom': classroom, 'topics': topics})

def topic_tasks(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    tasks = topic.task_set.all()
    return render(request, 'topic_tasks.html', {'topic': topic, 'tasks': tasks})

def task_text(request, task_id):
    task = Task.objects.get(pk=task_id)
    result = None

    if request.method == 'POST':
        selected_choice = request.POST.get('choice')
        if selected_choice == task.correct_answer:
            result = 'Correct!'
        else:
            result = 'Incorrect!'

    return render(request, 'task_text.html', {'task': task, 'result': result})

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

@staff_member_required(login_url='/')
def admin_panel(request):
    # Получение количества пользователей, задач, классов и тем
    user_count = User.objects.count()
    task_count = Task.objects.count()
    classroom_count = Classroom.objects.count()
    topic_count = Topic.objects.count()

    # Передача данных в шаблон
    return render(request, 'admin_templates/admin_panel.html', {
        'user_count': user_count,
        'task_count': task_count,
        'classroom_count': classroom_count,
        'topic_count': topic_count,
    })

@staff_member_required(login_url='/')
def class_info(request):
    classrooms = Classroom.objects.all()
    form = ClassroomForm()  # Initialize form outside of conditional blocks
    if request.method == 'POST':
        form = ClassroomForm(request.POST)  # Bind form data to form instance
        if 'create_class' in request.POST:
            if form.is_valid():
                form.save()
                return redirect('class_info')
        else:
            class_id = request.POST.get('class_id')
            if 'delete_class' in request.POST and class_id:
                classroom = get_object_or_404(Classroom, pk=class_id)
                classroom.delete()
                return redirect('class_info')
    return render(request, 'admin_templates/class_info.html', {'classrooms': classrooms, 'form': form})
    
@staff_member_required(login_url='/')
def edit_class(request, class_id):
    classroom = get_object_or_404(Classroom, pk=class_id)
    form = ClassroomForm(instance=classroom)
    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return redirect('class_info')
    return render(request, 'admin_templates/edit_class.html', {'form': form, 'classroom': classroom})

@staff_member_required(login_url='/')
def user_info(request):
    users = User.objects.all()
    return render(request, 'admin_templates/user_info.html', {'users': users})

@staff_member_required(login_url='/')
def topic_info(request):
    topics = Topic.objects.all()
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if 'create_topic' in request.POST:
            if form.is_valid():
                form.save()
                return redirect('topic_info')
        else:
            topic_id = request.POST.get('topic_id')
            if 'delete_topic' in request.POST and topic_id:
                topic = get_object_or_404(Topic, pk=topic_id)
                topic.delete()
                return redirect('topic_info')
    return render(request, 'admin_templates/topic_info.html', {'topics': topics, 'form': form})

@staff_member_required(login_url='/')
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    classrooms = Classroom.objects.all()
    form = TopicForm(instance=topic)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic_info')
    return render(request, 'admin_templates/edit_topic.html', {'classrooms': classrooms, 'form': form, 'topic': topic})

@staff_member_required(login_url='/')
def task_info(request):
    tasks = Task.objects.all()
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if 'create_task' in request.POST:
            if form.is_valid():
                form.save()
                return redirect('task_info')
        else: 
            task_id = request.POST.get('task_id')
            if 'delete_task' in request.POST and task_id:
                task = get_object_or_404(Task, pk=task_id)
                task.delete()
                return redirect('task_info')           
    return render(request, 'admin_templates/task_info.html', {'tasks': tasks, 'form': form})

@staff_member_required(login_url='/')
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    classrooms = Classroom.objects.all()
    topics = Topic.objects.all()
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_info')
    return render(request, 'admin_templates/edit_task.html', {'topics': topics,'classrooms': classrooms,'form': form, 'task': task})