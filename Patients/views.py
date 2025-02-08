from django.db.models import Q

from django.contrib.auth import logout

from django.contrib import messages
import uuid

from User.models import Login_user,Patient_reg
from django.shortcuts import render, redirect, get_object_or_404
from  Admin_app.models import DoctorReg,Department
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Appointment,PatientBilling
from datetime import datetime
from Doctor.models import DoctorSchedule,PatientMedicalRecord


from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home(request):
    return render(request,'Patient/home.html')


def department_view(request):
    # Check if the user is logged in
    if 'username' not in request.session:
        return redirect('Login')

    username = request.session['username']

    user = get_object_or_404(Patient_reg, Username=username)

    departments = Department.objects.all()

    for dep in departments:
        print(dep.Department_name, dep.description, dep.image)

    return render(request, 'Patient/department_view.html', {'departments': departments, 'user': user})



def department_singleview(request, dep_id):
    username = request.session.get('username')

    user = get_object_or_404(Patient_reg, Username=username)

    departments = Department.objects.filter(id=dep_id)

    if not departments.exists():
        return render(request, 'Patient/department_not_found.html', {'user': user})

    return render(request, 'Patient/department_singleview.html', {'departments': departments, 'user': user})




def create_appointment(request):
    username = request.session.get('username')
    if not username:
        return redirect('/User/Login/')

    user = get_object_or_404(Patient_reg, Username=username)  # Fetch patient by username

    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')  # This will now be filled automatically
        department_id = request.POST.get('department')
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason_for_visit = request.POST.get('reason_for_visit')

        # Validate all required fields
        if not all([patient_name, department_id, doctor_id, date, time]):
            return HttpResponse(
                "<script>alert('All fields are required!');window.location='/Patients/create_appointment';</script>"
            )

        try:
            # Convert time string to HH:MM format
            formatted_time = datetime.strptime(time, "%H:%M").time()

            appointment = Appointment.objects.create(
                patient_name=user,  # This links the appointment to the logged-in patient
                department=Department.objects.get(id=department_id),
                doctor=DoctorReg.objects.get(id=doctor_id),
                date=date,
                time=formatted_time,  # Store properly formatted time
                reason_for_visit=reason_for_visit,
            )
            return HttpResponse(
                "<script>alert('Appointment created successfully!');window.location='/Patients/appointment_success';</script>"
            )
        except Exception as e:
            print(f"Error creating appointment: {e}")
            return HttpResponse(
                "<script>alert('An error occurred while creating the appointment.');window.location='/Patients/create_appointment';</script>"
            )

    else:
        departments = Department.objects.all()
        return render(request, 'Patient/appointment.html', {
            'departments': departments,
            'user': user,  # Pass the user object to the template for patient name
        })
def fill_doctors(request):
        department = request.POST.get("department")
        doctors = DoctorReg.objects.filter(department=department).values('id', 'D_name')
        return JsonResponse(list(doctors), safe=False)


def doctors_view(request):
    username = request.session.get('username')
    user = get_object_or_404(Patient_reg, Username=username)

    search_query = request.GET.get('search', '')  # Get search query from request
    if search_query:
        doctors = DoctorReg.objects.filter(department__Department_name__icontains=search_query)
    else:
        doctors = DoctorReg.objects.all()

    return render(request, 'Patient/doctors_view.html', {'user': user, 'doctors': doctors, 'search_query': search_query})


def doctor_singleview(request, doc_id):
    username = request.session.get('username')

    user = get_object_or_404(Patient_reg, Username=username)
    doctor = get_object_or_404(DoctorReg, id=doc_id)  # Get specific doctor
    schedules = DoctorSchedule.objects.filter(doctor=doc_id)  # Filter schedules

    return render(request, 'Patient/doctor_singleview.html', {'doctor': doctor, 'schedules': schedules})


def appointment_success(request):
    return render(request,'Patient/appointment_success.html')


def view_completed_appointment(request):
    username = request.session.get('username')

    user = get_object_or_404(Patient_reg, Username=username)

    try:
        # Get the logged-in doctor
        patient = Patient_reg.objects.get(Username=username)

        # Get only this doctor's Scheduled & Completed appointments
        appo = Appointment.objects.filter(
            Q(status="Completed")| Q(status="Scheduled"),
            patient_name=patient
        ).order_by('-date')

    except DoctorReg.DoesNotExist:
        appo = None  # No appointments, doctor not found
        messages.success(request, "Appointment has been successfully completed.")  # Success message

    return render(request, 'Patient/appointment_completed.html', {"appo": appo})


def medical_records_list(request):
    username = request.session.get('username')

    # Ensure the user is logged in
    if not username:
        return render(request, {'message': 'User not logged in'})

    # Retrieve the patient object based on the logged-in username
    patient = get_object_or_404(Patient_reg, Username=username)

    # Fetch medical records for the patient
    medical_records = PatientMedicalRecord.objects.filter(patient_name=patient)

    return render(request, 'Patient/medical_record_view.html', {
        'medical_records': medical_records,
        'patient': patient,  # Pass patient details
    })




def generate_billing_id():
    """Generate a unique billing ID"""
    return f"BILL-{uuid.uuid4().hex[:10].upper()}"

def billing_details(request):
    username = request.session.get('username')

    # Ensure user is logged in
    if not username:
        return render(request, 'error.html', {'message': 'User not logged in'})

    # Fetch patient details
    patient = get_object_or_404(Patient_reg, Username=username)

    # Retrieve or create a billing record for the patient
    billing_record, created = PatientBilling.objects.get_or_create(
        patient=patient,
        defaults={
            'billing_id': generate_billing_id(),
            'amount_due': 0.00,  # Default value, update as needed
        }
    )

    return render(request, 'Patient/payment.html', {
        'billing': billing_record,
        'patient': patient,
    })


def process_payment(request):
    if request.method == 'POST':
        billing_id = request.POST.get('billing_id')
        payment_method = request.POST.get('payment_method')
        amount_due = request.POST.get('amount_due')
        insurance_details = request.POST.get('insurance_details', '')

        # ❌ Check if payment_method is empty
        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return redirect('billing_details')

        # Fetch the billing record
        billing_record = get_object_or_404(PatientBilling, billing_id=billing_id)

        # Update billing details
        billing_record.payment_method = payment_method
        billing_record.amount_due = amount_due
        billing_record.insurance_details = insurance_details
        billing_record.payment_status = 'Paid'
        billing_record.save()

        messages.success(request, "Payment Successful!")
        return redirect('billing_details')

    return redirect('billing_details')

def user_logout(request):
    logout(request)
    return redirect('U_home')


def health_tips(request):
    return render(request,'Patient/health_tips.html')
