import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

def generate_filename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{extension}"
    return os.path.join('profile_pic', new_filename) 


def generate_filename2(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{extension}"
    return os.path.join('topic_images', new_filename)


def generate_video_filename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{extension}"
    return os.path.join('topic_videos', new_filename)

# class Task(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     completed = models.BooleanField(default=False)
#     completion_date = models.DateField()

#     def __str__(self):
#         return self.name

class Classroom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def total_tasks(self):
        return self.task_set.count()

    
class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    images = models.ManyToManyField('Image', blank=True)
    videos = models.ManyToManyField('Video', blank=True)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Бірнеше Таңдау Туралы Сұрақ'),
        ('TF', 'Шын / Жалған Сұрақ'),
        ('OQ', 'Ашық Сұрақ'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=255, null=True, blank=True)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='MCQ')
    choice1 = models.CharField(max_length=100, blank=True)
    choice2 = models.CharField(max_length=100, blank=True)
    choice3 = models.CharField(max_length=100, blank=True)
    choice4 = models.CharField(max_length=100, blank=True)
    correct_answer = models.CharField(max_length=100, choices=[('choice1', 'Таңдау 1'), ('choice2', 'Таңдау 2'), ('choice3', 'Таңдау 3'), ('choice4', 'Таңдау 4')], null=True, blank=True)

    def __str__(self):
        return self.question
    



    


class ClassroomProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    progress_percentage = models.IntegerField(default=0)
    completed_tasks_count = models.IntegerField(default=0)
    completed_tasks = models.ManyToManyField(Task, related_name='completed_in_classroom')

    def __str__(self):
        return f"{self.user.username} - {self.classroom.name}"
    

class Custom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=generate_filename, null=True, blank=True, default="profile_pic/default.png")

    # progress_percentage = models.IntegerField(default=0)
    # completed_tasks_count = models.IntegerField(default=0)
    # completed_tasks = models.ManyToManyField(Task, related_name='completed_by')
    # classroom_progress = models.ManyToManyField(ClassroomProgress, related_name='user_progress')

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name
    
class Image(models.Model):
    image = models.ImageField(upload_to=generate_filename2, null=True, blank=True)

    def __str__(self):
        return self.image.name

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    
    def get_session_duration(self):
        if self.logout_time:
            return (self.logout_time - self.login_time).total_seconds() / 60  # duration in minutes
        return 0
    


class Video(models.Model):
    video = models.FileField(upload_to=generate_video_filename, null=True, blank=True)

    def __str__(self):
        return self.video.name





