from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-student/', views.add_student, name='add-student'),
    path('add-teacher/', views.add_teacher, name='add-teacher')
]
