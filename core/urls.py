from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('add-student/', views.add_student, name='add-student'),
    # path('add-teacher/', views.add_teacher, name='add-teacher')
    path('teacher-admin/', views.teacher, name='teacher_admin'),
    path('view-teachers/', views.view_teachers, name='view_teachers'),
    path('add-teachers/', views.add_teachers, name='add_teachers'),
    path('update-teacher/<int:teacher_id>/', views.update_teacher, name='update_teacher'),
    path('delete-teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),


    path('student-admin/', views.student, name='student_admin'),
    path('view-students/', views.view_students, name='view_students'),
    path('add-student/', views.add_student, name='add_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('update-student/<int:student_id>/', views.update_student, name='update_student'),

    path('attendance/', views.attendance, name='attendance'),
    path('select-date-class/', views.select_date_class, name='select_date_class'),
    path('mark-attendance/<int:class_id>/<str:attendance_date>/', views.mark_attendance, name='mark_attendance'),
]
