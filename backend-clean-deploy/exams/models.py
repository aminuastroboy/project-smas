from django.db import models
from django.conf import settings
class Subject(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self): return self.name
class Topic(models.Model):
    name = models.CharField(max_length=150)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    def __str__(self): return f"{self.subject.name} - {self.name}"
class Exam(models.Model):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    classroom = models.ForeignKey('users.ClassRoom', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    total_marks = models.IntegerField(default=100)
    auto_grade = models.BooleanField(default=True)
    def __str__(self): return self.title
class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    marks = models.IntegerField(default=1)
    is_mcq = models.BooleanField(default=True)
    options = models.JSONField(blank=True, null=True)
    correct_answer = models.CharField(max_length=512, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self): return f"Q{self.id} ({self.exam.title})"
class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    total_score = models.FloatField(default=0)
    percent = models.FloatField(default=0)
    breakdown = models.JSONField(default=dict)
    career_advice = models.JSONField(default=list)
    graded = models.BooleanField(default=False)
    graded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
