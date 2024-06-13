from django.contrib import admin
from .models import FeePayment, FeePaymentItem, FeeType, Notice, Student, Teacher, Class, StudentAttendance, TeacherAttendance, TeacherSalaryPayment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'class_name', 'monthly_fee', 'address', 'contact_no')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'salary', 'contact_no', 'address')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'date', 'present')

@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'date', 'present')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'date', 'added_by')
    
@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'payment_date', 'total_amount', 'payment_status')
    list_filter = ('payment_status', 'payment_date')
    search_fields = ('student__name',)

@admin.register(FeePaymentItem)
class FeePaymentItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'fee_payment', 'fee_type', 'amount')
    list_filter = ('fee_payment__student__name', 'fee_type')
    search_fields = ('fee_payment__student__name', 'fee_type__name')
    
@admin.register(TeacherSalaryPayment)
class TeacherSalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'payment_date', 'amount_paid')
    list_filter = ('payment_date',)
    search_fields = ('teacher__name',)
