from datetime import date, datetime
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Student, StudentAttendance, Teacher, Class, TeacherSalaryPayment
from django.contrib import messages
from .models import FeePayment, Notice
from django.db.models import Sum, F

# Create your views here.
@login_required(login_url='/auth/login/')
def dashboard(request):
    # Count of students and teachers
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()

    # Total salary of all teachers
    total_teacher_salary = Teacher.objects.aggregate(total=Sum('salary'))['total'] or 0

    # Total fees paid by students
    total_student_fees = FeePayment.objects.filter(payment_status=True).aggregate(total=Sum('total_amount'))['total'] or 0

    unpaid_salaries = TeacherSalaryPayment.objects.filter(is_paid=False)
    total_pending_salaries = unpaid_salaries.aggregate(total_pending=Sum(F('teacher__salary') - F('amount_paid')))['total_pending'] or 0

    # All notices
    all_notices = Notice.objects.all()

    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'total_teacher_salary': total_teacher_salary,
        'total_student_fees': total_student_fees,
        'all_notices': all_notices,
        'total_pending_salaries': total_pending_salaries,
    }
    return render(request, 'admin-dashboard.html', context)
    
@login_required(login_url='/auth/login/')
def teacher(request):
    return render(request, 'admin-teacher.html')

@login_required(login_url='/auth/login/')
def view_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'admin-view-teachers.html', {'teachers': teachers})

@login_required(login_url='/auth/login/')
def add_teachers(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        contact_no = request.POST.get('contact_no')
        salary = request.POST.get('salary')
        address = request.POST.get('address')
        class_ids = request.POST.getlist('classes')

        try:
            # Create a User instance
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)

            # Create a Teacher instance linked to this user
            teacher = Teacher.objects.create(
                user=user,
                name=f"{first_name} {last_name}",
                contact_no=contact_no,
                salary=salary,
                address=address
            )

            # Link selected classes to the teacher
            teacher.classes.set(Class.objects.filter(id__in=class_ids))
            teacher.save()

            messages.success(request, 'Teacher added successfully!')
            return redirect('/view-teachers')  # Redirect to teacher list page after successful creation

        except IntegrityError:
            messages.error(request, 'Username already exists. Please choose a different username.')
            classes = Class.objects.all()
            return render(request, 'admin-add-teacher.html', {'classes': classes})

    else:
        classes = Class.objects.all()
        return render(request, 'admin-add-teacher.html', {'classes': classes})

@login_required(login_url='/auth/login/')
def update_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    classes = Class.objects.all()  # Assuming you have a Class model

    if request.method == 'POST':
        # Retrieve updated data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        classes_ids = request.POST.getlist('classes')  # Assuming classes are selected as a list of IDs
        salary = request.POST.get('salary')
        contact_no = request.POST.get('contact_no')
        address = request.POST.get('address')

        # Update user instance with new first name and last name
        user = teacher.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Update teacher instance with new data
        teacher.name = f"{first_name} {last_name}"  # Set full name in Teacher model
        teacher.classes.clear()  # Clear existing classes
        teacher.classes.add(*classes_ids)  # Add new selected classes
        teacher.salary = salary
        teacher.contact_no = contact_no
        teacher.address = address
        teacher.save()

        messages.success(request, f'Teacher "{teacher.name}" has been updated.')
        return redirect('/view-teachers')  # Redirect to teacher list page after update

    # Render the update form with existing data
    return render(request, 'admin-update-teacher.html', {'teacher': teacher, 'classes': classes})

@login_required(login_url='/auth/login/')
def delete_teacher(request, teacher_id):
    # Retrieve the teacher object or return 404 if not found
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        # Delete associated user (assuming OneToOneField with User model)
        user = teacher.user
        user.delete()

        messages.success(request, f'Teacher "{teacher.get_name}" has been deleted.')
        return redirect('/view-teachers')  # Redirect to teacher list page after deletion
    return redirect('/view-teachers')

@login_required(login_url='/auth/login/')
def student(request):
    return render(request, 'admin-student.html')

@login_required(login_url='/auth/login/')
def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        class_id = request.POST.get('class_name')
        monthly_fee = request.POST.get('monthly_fee')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')

        if not name or not class_id or not monthly_fee or not address or not contact_no:
            messages.error(request, 'All fields are required.')
        else:
            class_instance = Class.objects.get(id=class_id)
            Student.objects.create(
                name=name,
                class_name=class_instance,
                monthly_fee=monthly_fee,
                address=address,
                contact_no=contact_no
            )
            messages.success(request, 'Student has been added successfully.')
            return redirect('/view-students')
    
    classes = Class.objects.all()
    return render(request, 'admin-add-student.html', {'classes': classes})

@login_required(login_url='/auth/login/')
def view_students(request):
    students = Student.objects.all()
    return render(request, 'admin-view-students.html', {'students': students})

@login_required(login_url='/auth/login/')
def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        name = request.POST['name']
        class_name_id = request.POST['class_name']
        monthly_fee = request.POST['monthly_fee']
        address = request.POST['address']
        contact_no = request.POST['contact_no']
        
        # Update student instance with new data
        student.name = name
        student.class_name = get_object_or_404(Class, id=class_name_id)
        student.monthly_fee = monthly_fee
        student.address = address
        student.contact_no = contact_no
        student.save()

        messages.success(request, 'Student updated successfully.')
        return redirect('/view_students')
    
    classes = Class.objects.all()
    return render(request, 'admin-update-student.html', {'student': student, 'classes': classes})

@login_required(login_url='/auth/login/')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('/view-students')
    return redirect('/view-students')

@login_required(login_url='/auth/login/')
def attendance(request):
    return render(request, 'attendance.html')

@login_required(login_url='/auth/login/')
def select_date_class(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        date_selected = request.POST.get('date')

        if class_id and date_selected:
            return redirect('mark_attendance', class_id=class_id, date_selected=date_selected)

        messages.error(request, 'Please select both date and class.')

    classes = Class.objects.all()
    context = {
        'classes': classes,
    }
    return render(request, 'select_date_class.html', context)

@login_required(login_url='/auth/login/')
def mark_attendance(request, class_id, attendance_date):
    selected_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(class_name=selected_class)

    # Convert attendance_date from string to datetime object
    attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()

    # Create a dictionary to store attendance status for each student
    attendance_status = {}
    for student in students:
        try:
            attendance = student.studentattendance_set.get(date=attendance_date)
            attendance_status[student.id] = attendance.present
        except StudentAttendance.DoesNotExist:
            attendance_status[student.id] = False  # Default to False if no attendance record exists

    context = {
        'selected_class': selected_class,
        'attendance_date': attendance_date,
        'students': students,
        'attendance_status': attendance_status,
    }

    return render(request, 'mark-attendance.html', context)