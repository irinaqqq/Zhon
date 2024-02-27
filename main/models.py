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

class Custom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=generate_filename, null=True, blank=True, default="profile_pic/default.png")

    progress_percentage = models.IntegerField(default=0)
    completed_tasks_count = models.IntegerField(default=0)

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    completion_date = models.DateField()

    def __str__(self):
        return self.name
    

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name