from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    is_guardian = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    phone = models.CharField(max_length=30, blank=True, null=True)
class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    guardian = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='wards')
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self): return self.user.get_full_name()
