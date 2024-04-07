"""
URL configuration for ZhonEdu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'classrooms', views.ClassroomViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'classroom-progress', views.ClassroomProgressViewSet)
router.register(r'customs', views.CustomViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('classroom/', views.classroom_view, name='classroom'),
    path('classrooms/<int:classroom_id>/topics/', views.classroom_topics, name='classroom_topics'),
    path('topics/<int:topic_id>/tasks/', views.topic_tasks, name='topic_tasks'),
    path('tasks/<int:task_id>/', views.task_text, name='task_text'),
    path('', views.home_view, name='home'),
    path('library/', views.library_view, name='library'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('class_info/', views.class_info, name='class_info'),
    path('class_info/<int:class_id>/edit/', views.edit_class, name='edit_class'),
    path('user_info/', views.user_info, name='user_info'),
    path('topic_info/', views.topic_info, name='topic_info'),
    path('topic_info/<int:topic_id>/edit/', views.edit_topic, name='edit_topic'),
    path('task_info/', views.task_info, name='task_info'),
    path('task_info/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('get_topics_by_classroom/<int:classroom_id>/', views.get_topics_by_classroom, name='get_topics_by_classroom'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
