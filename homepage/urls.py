from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('faculty/', views.faculty, name='faculty'),
    path('student/', views.student, name='student'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact')
]
