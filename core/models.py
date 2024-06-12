from django.db import models

# Create your models here.

class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    admission_charge = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    contact_no = models.CharField(max_length=12)
    attendance = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    classes = models.ManyToManyField(Class)
    salary = models.DecimalField(max_digits=15, decimal_places=2)
    attendance = models.PositiveIntegerField()
    contact_no = models.CharField(max_length=12)
    address = models.TextField()

    def __str__(self):
        return self.name
