from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Class(models.Model):
    CLASS_CHOICES = [
        ("Class 1", "Class 1"),
        ("Class 2", "Class 2"),
        ("Class 3", "Class 3"),
        ("Class 4", "Class 4"),
        ("Class 5", "Class 5"),
        ("Class 6", "Class 6"),
        ("Class 7", "Class 7"),
        ("Class 8", "Class 8"),
        ("Class 9", "Class 9"),
        ("Class 10", "Class 10"),
        ("Class 11", "Class 11"),
        ("Class 12", "Class 12"),
    ]

    name = models.CharField(max_length=100, choices=CLASS_CHOICES, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    # admission_charge = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    contact_no = models.CharField(max_length=12)

    def __str__(self):
        return self.name

    @property
    def get_id(self):
        return self.user.id

    @property
    def get_name(self):
        return self.user.get_full_name() if self.user.get_full_name() else self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    classes = models.ManyToManyField(Class)
    salary = models.DecimalField(max_digits=15, decimal_places=2)
    contact_no = models.CharField(max_length=12)
    address = models.TextField()

    def __str__(self):
        return self.name

    @property
    def get_id(self):
        return self.user.id

    @property
    def get_name(self):
        return self.user.get_full_name() if self.user.get_full_name() else self.name


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.date}"


class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.teacher.name} - {self.date}"


class Notice(models.Model):
    date = models.DateField(auto_now=True)
    added_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)


# class Fee(models.Model):
#     fee_choices = [
#         ('Admission Charge', 'Admission Charge'),
#         ('Monthly Fee', 'Monthly Fee'),
#         ('Exam Fee', 'Exam Fee'),
#         ('Miscellaneous', 'Miscellaneous'),
#     ]
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     due_date = models.DateField()
#     paid = models.BooleanField(default=False)
#     fee_type = models.CharField(max_length=100, choices=fee_choices)

#     def __str__(self):
#         return f"{self.student.name} - {self.amount} - {self.due_date}"


class FeeType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.payment_date}"


class FeePaymentItem(models.Model):
    fee_payment = models.ForeignKey(FeePayment, on_delete=models.CASCADE)
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.fee_payment.student.name} - {self.fee_type.name} - {self.amount}"

class TeacherSalaryPayment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    payment_date = models.DateField(default=date.today)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.teacher.name} - {self.payment_date} - {'Paid' if self.is_paid else 'Unpaid'}"