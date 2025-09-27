from django.db import models
from users.models import Student
class FeeStructure(models.Model):
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    applicable_to = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self): return f"{self.name} - {self.amount}"
class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    reference = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
