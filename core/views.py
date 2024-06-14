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
    all_notices = Notice.objects.all().order_by('-date')

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
def select_class(request, type):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        if class_id:
            # Redirect to the page for taking attendance for the selected class
            if type == 'mark':
                return redirect(f'/mark-attendance/{class_id}/')
            elif type == 'list':
                return redirect(f'/attendance-list/{class_id}/')
        else:
            # Handle case where no class is selected (though should be handled by required attribute in HTML)
            # You can customize this based on your specific needs
            return render(request, 'select_class.html', {'classes': Class.objects.all()})
    return render(request, 'select_class.html', {'classes': Class.objects.all()})

@login_required(login_url='/auth/login/')
def mark_attendance(request, class_id):
    selected_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(class_name=selected_class)
    
    if request.method == 'POST':
        for student in students:
            present = request.POST.get(f'student_{student.id}') == 'present'
            attendance_record, created = StudentAttendance.objects.get_or_create(
                student=student,
                date=date.today(),
                defaults={'present': present}
            )
            if not created:
                attendance_record.present = present
                attendance_record.save()
        
        return redirect('/attendance')

    context = {
        'selected_class': selected_class,
        'students': students,
    }
    return render(request, 'mark-attendance.html', context)

@login_required(login_url='/auth/login/')
def attendance_list(request, class_id):
    selected_class = get_object_or_404(Class, id=class_id)
    date_str = request.GET.get('date', '')  # Get date from query parameter
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert date string to datetime.date
        except ValueError:
            date = None
    else:
        date = None
    
    if date:
        # Retrieve attendance records for the selected class and date
        attendance_records = StudentAttendance.objects.filter(student__class_name=selected_class, date=date)
    else:
        attendance_records = []

    context = {
        'selected_class': selected_class,
        'attendance_records': attendance_records,
        'selected_date': date_str,  # Pass the selected date to the template
    }
    return render(request, 'attendance-list.html', context)

@login_required(login_url='/auth/login/') 
def add_notice_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Assuming you have authentication and request.user is a Teacher instance
        added_by = request.user.teacher
        
        # Create the notice object
        notice = Notice.objects.create(
            title=title,
            description=description,
            added_by=added_by,
            date=date.today()
        )
        
        messages.success(request, 'Notice added successfully.')
        return redirect('/dashboard')  # Replace 'dashboard' with your actual dashboard URL name
    else:
        return render(request, 'add_notice.html')