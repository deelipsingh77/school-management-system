from django.shortcuts import redirect, render

def home(request):
    return render(request, 'index.html')

def faculty(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'faculty-portal.html')

def student(request):
    return render(request, 'student-portal.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

