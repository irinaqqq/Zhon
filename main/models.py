import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

def generate_filename(instance, filename):
    extension = filename.split('.')[-1]
    # Generate a unique filename using UUID
    new_filename = f"{uuid.uuid4().hex}.{extension}"
    return os.path.join('profile_pic', new_filename)



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
    
class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Task(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Question'),
        ('TF', 'True/False Question'),
        ('OQ', 'Open Question'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=255, null=True, blank=True)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='MCQ')
    choice1 = models.CharField(max_length=100, blank=True)
    choice2 = models.CharField(max_length=100, blank=True)
    choice3 = models.CharField(max_length=100, blank=True)
    choice4 = models.CharField(max_length=100, blank=True)
    correct_answer = models.CharField(max_length=100, choices=[('choice1', 'Choice 1'), ('choice2', 'Choice 2'), ('choice3', 'Choice 3'), ('choice4', 'Choice 4')], null=True, blank=True)

    def __str__(self):
        return self.question
    


class Custom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=generate_filename, null=True, blank=True, default="profile_pic/default.png")

    progress_percentage = models.IntegerField(default=0)
    completed_tasks_count = models.IntegerField(default=0)
    completed_tasks = models.ManyToManyField(Task, related_name='completed_by')

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name
    