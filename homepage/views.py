from django.shortcuts import redirect, render

from core.models import Notice

def home(request):
    all_notices = Notice.objects.all().order_by('-date')
    return render(request, 'index.html', {"all_notices": all_notices})

def faculty(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'faculty-portal.html')

def student(request):
    return render(request, 'student-portal.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    all_notices = Notice.objects.all().order_by('-date')
    return render(request, 'contact.html', {"all_notices": all_notices})


