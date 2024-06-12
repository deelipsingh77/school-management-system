from django.contrib import admin
from .models import Student, Teacher, Class

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_classes_display', 'salary', 'attendance', 'contact_no', 'address')

    def get_classes_display(self, obj):
        return ", ".join([class_obj.name for class_obj in obj.classes.all()])

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name', 'admission_charge', 'monthly_fee', 'address', 'contact_no', 'attendance')

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Class, ClassAdmin)