from django.shortcuts import render,redirect,get_object_or_404
from .forms import Department_form,DoctorRegForm
from django.contrib import messages,auth
from User.models import Login_user,Patient_reg
from django.core.paginator import Paginator,EmptyPage
from  .models import DoctorReg,Department
from  Patients.models import Appointment
from django.contrib.auth import logout



# Create your views here.
def home(request):
    return render(request,'Admin/index.html')


def department(request):
    if request.method == 'POST':
        form = Department_form(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('department')  # Replace with your desired redirect URL
    else:
        form = Department_form()

    return render(request, 'Admin/department.html', {'form': form})

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegForm(request.POST, request.FILES)

        if form.is_valid():
            # Save the doctor details to the Doctor_reg table
            doctor = form.save(commit=False)

            # Extract required fields for the login table
            Username = form.cleaned_data.get('username')  # Ensure this field exists in the form
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            # Validate that passwords match
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'Admin/doctor_reg.html', {'form': form})

            # Check if the username or email already exists
            if Login_user.objects.filter(Username=Username).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
                return render(request, 'Admin/doctor_reg.html', {'form': form})

            # Save doctor data to the database
            doctor.save()

            # Create and save a login table entry for the doctor
            login_table = Login_user(
                Username=Username,
                password1=password1,
                password2=password2,
                type='doctor'
            )
            login_table.save()

            messages.success(request, 'Doctor registration successful')
            return redirect('success_page')  # Replace with your desired redirect URL

        else:
            messages.error(request, 'Please correct the errors in the form.')

    else:
        form = DoctorRegForm()

    return render(request, 'Admin/doctor_reg.html', {'form': form})


def success_page(request):
    return render(request, 'Admin/success_page.html')


def patient_view(request):

    details=Patient_reg.objects.all()

    # Instantiate the Paginator with the queryset and number of items per page
    paginator = Paginator(details, 4)
    page_number = request.GET.get('page')  # Get the page number from the request

    try:
        # Get the specific page of results
        page = paginator.get_page(page_number)
    except EmptyPage:
        # Handle the case where the page is out of range
        page = paginator.page(paginator.num_pages)

    # Pass the paginated results to the template

    return render(request,'Admin/patients_view.html',{'details':details,'page': page})


def deletepatient(request, user_id):
    try:
        user = Patient_reg.objects.get(id=user_id)
    except Patient_reg.DoesNotExist:
        # Handle case where book does not exist
        return redirect('patient_view')  # Redirect to a book list page or another page

    if request.method == 'POST':
        user.delete()  # Delete the book if the request is POST
        return redirect('patient_view')  # Redirect to the home page or book list after deletion

    return render(request, 'Admin/deletepatient.html', {'user': user})  # Render the confirmation pageder(request,'delete.html', {'book':book})


def doctor_view(request):

    details=DoctorReg.objects.all()

    # Instantiate the Paginator with the queryset and number of items per page
    paginator = Paginator(details, 4)
    page_number = request.GET.get('page')  # Get the page number from the request

    try:
        # Get the specific page of results
        page = paginator.get_page(page_number)
    except EmptyPage:
        # Handle the case where the page is out of range
        page = paginator.page(paginator.num_pages)

    # Pass the paginated results to the template

    return render(request,'Admin/doctors_view.html',{'details':details,'page': page})


def deletedoctor(request, doctor_id):
    try:
        doctor = DoctorReg.objects.get(id=doctor_id)
    except DoctorReg.DoesNotExist:
        # Handle case where book does not exist
        return redirect('doctor_view')  # Redirect to a book list page or another page

    if request.method == 'POST':
        doctor.delete()  # Delete the book if the request is POST
        return redirect('doctor_view')  # Redirect to the home page or book list after deletion

    return render(request, 'Admin/deletedoctors.html', {'doctor': doctor})  # Render the confirmation pageder(request,'delete.html', {'book':book})


def department_view(request):

    details=Department.objects.all()

    # Instantiate the Paginator with the queryset and number of items per page
    paginator = Paginator(details, 4)
    page_number = request.GET.get('page')  # Get the page number from the request

    try:
        # Get the specific page of results
        page = paginator.get_page(page_number)
    except EmptyPage:
        # Handle the case where the page is out of range
        page = paginator.page(paginator.num_pages)

    # Pass the paginated results to the template

    return render(request,'Admin/department_view.html',{'details':details,'page': page})


def deletedepartment(request, department_id):
    try:
        department = Department.objects.get(id=department_id)
    except Department.DoesNotExist:
        # Handle case where book does not exist
        return redirect('department_view')  # Redirect to a book list page or another page

    if request.method == 'POST':
        department.delete()  # Delete the book if the request is POST
        return redirect('department_view')  # Redirect to the home page or book list after deletion

    return render(request, 'Admin/deletedepartment.html', {'department': department})  # Render the confirmation pageder(request,'delete.html', {'book':book})


def appointment_view(request):

    details=Appointment.objects.all()

    # Instantiate the Paginator with the queryset and number of items per page
    paginator = Paginator(details, 4)
    page_number = request.GET.get('page')  # Get the page number from the request

    try:
        # Get the specific page of results
        page = paginator.get_page(page_number)
    except EmptyPage:
        # Handle the case where the page is out of range
        page = paginator.page(paginator.num_pages)

    # Pass the paginated results to the template

    return render(request,'Admin/appointment.html',{'details':details,'page': page})



def user_logout(request):
    logout(request)
    return redirect('U_home')