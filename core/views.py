from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Student, Teacher, Class
from django.contrib import messages

# Create your views here.
@login_required(login_url='/auth/login/')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/auth/login/')
def home(request):
    return redirect('dashboard')
    
@login_required(login_url='/auth/login/')
def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        class_id = request.POST.get('class_name')
        admission_charge = request.POST.get('admission_charge')
        monthly_fee = request.POST.get('monthly_fee')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        attendance = request.POST.get('attendance')

        # Fetch the class instance
        class_instance = Class.objects.get(id=class_id)

        # Save the student to the database
        Student.objects.create(
            name=name,
            class_name=class_instance,
            admission_charge=admission_charge,
            monthly_fee=monthly_fee,
            address=address,
            contact_no=contact_no,
            attendance=attendance
        )

        # Add success message
        messages.success(request, 'Student data saved successfully!')

        return redirect('add-student')

    # Retrieve all classes for displaying in the form
    classes = Class.objects.all()

    return render(request, 'add-student.html', {'classes': classes})

@login_required(login_url='/auth/login/')
def add_teacher(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        salary = request.POST.get('salary')
        attendance = request.POST.get('attendance')
        contact_no = request.POST.get('contact_no')
        address = request.POST.get('address')
        classes_ids = request.POST.getlist('classes')

        classes = Class.objects.filter(pk__in=classes_ids)

        teacher = Teacher.objects.create(
            name=name,
            salary=salary,
            attendance=attendance,
            contact_no=contact_no,
            address=address
        )
        teacher.classes.add(*classes)

        messages.success(request, 'Teacher data saved successfully!')

        return redirect('add-teacher')

    classes = Class.objects.all()

    return render(request, 'add-teacher.html', {'classes': classes})