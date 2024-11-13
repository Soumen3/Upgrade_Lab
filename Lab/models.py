from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class institue(models.Model):
#     name = models.CharField(max_length=1000)
#     location = models.CharField(max_length=1000)
#     phone = models.IntegerField(null=True, blank=True)
class UserDetail(models.Model):
    TEACHER = 'teacher'
    STUDENT = 'student'

    ROLE_CHOICES = [
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=True)
    institute = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username