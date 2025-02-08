from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib import messages
from .forms import EPrescriptionForm
from Admin_app.forms import Department,DoctorReg
from django.contrib.auth.decorators import login_required
from Patients.models import Appointment
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import DoctorSchedule, DoctorReg
from datetime import datetime
from django.contrib.auth import logout
from .models import PatientMedicalRecord
from .forms import PatientMedicalRecordForm


# Create your views here.

def home(request):
    return render(request,'Doctor/home.html')

def prescription_create(request):
    if request.method == 'POST':
        form = EPrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prescription_list')  # Redirect to the list view after saving
    else:
        form = EPrescriptionForm()
    return render(request, 'Doctor/prescription_form.html', {'form': form})





# View to display all schedules
def list_schedules(request):
    schedules = DoctorSchedule.objects.all().order_by('available_date', 'time_slot','time_end_slot')
    return render(request, 'Doctor/list_schedules.html', {'schedules': schedules})


def create_schedule(request):
    if 'username' not in request.session:
        return redirect('Login')

    username = request.session['username']
    user = get_object_or_404(DoctorReg, username=username)

    doctors = DoctorReg.objects.all()  # Fetch all doctors for the dropdown

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        available_date = request.POST.get('available_date')
        time_slot = request.POST.get('time_slot')
        time_end_slot = request.POST.get('time_end_slot')  # Added field
        special_notes = request.POST.get('special_notes', '')

        # Validation
        if not all([doctor_id, available_date, time_slot, time_end_slot]):
            return HttpResponse(
                "<script>alert('Please fill out all required fields.');window.location='/schedules/create/';</script>"
            )

        try:
            # Convert date and time to the correct format
            available_date = datetime.strptime(available_date, '%Y-%m-%d').date()
            time_slot = datetime.strptime(time_slot, '%H:%M').time()
            time_end_slot = datetime.strptime(time_end_slot, '%H:%M').time()

            # Check if end time is after start time
            if time_end_slot <= time_slot:
                return HttpResponse(
                    "<script>alert('End time must be after the start time.');window.location='/schedules/create/';</script>"
                )

            # Create the schedule
            DoctorSchedule.objects.create(
                doctor=DoctorReg.objects.get(id=doctor_id),
                available_date=available_date,
                time_slot=time_slot,
                time_end_slot=time_end_slot,  # Added field
                special_notes=special_notes,
            )
            return HttpResponse(
                "<script>alert('Schedule created successfully!');window.location='list_schedules';</script>"
            )
        except Exception as e:
            print(f"Error creating schedule: {e}")
            return HttpResponse(
                "<script>alert('An error occurred while creating the schedule.');window.location='Doctor/schedules/create/';</script>"
            )

    return render(request, 'Doctor/create_schedule.html', {'doctors': doctors, 'user': user, 'selected_doctor': user.id})

def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(DoctorSchedule, id=schedule_id)
    if request.method == 'POST':
        schedule.delete()
        return redirect('list_schedules')  # Redirect to the list view
    return render(request, 'Doctor/delete_schedule.html', {'schedule': schedule})



def doctors(request):
    username = request.session.get('username')

    user = get_object_or_404(DoctorReg, username=username)

    doctors = DoctorReg.objects.all()
    for doc in doctors:
        print(doc.D_name, doc.department, doc.photo,doc.phone)

    return render(request,'Doctor/doctors.html',{'user':user, 'doctors':doctors})



def view_department(request):
    # Check if the user is logged in
    if 'username' not in request.session:
        return redirect('Login')

    username = request.session['username']

    user = get_object_or_404(DoctorReg, username=username)

    departments = Department.objects.all()

    for dep in departments:
        print(dep.Department_name, dep.description, dep.image)

    return render(request, 'Doctor/view_department.html', {'departments': departments, 'user': user})



def singleview_department(request, dep_id):
    username = request.session.get('username')

    user = get_object_or_404(DoctorReg, username=username)

    departments = Department.objects.filter(id=dep_id)

    if not departments.exists():
        return render(request, 'Doctor/department_not_found.html', {'user': user})

    return render(request, 'Doctor/singleview_department.html', {'departments': departments, 'user': user})


def view_appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Restrict access: Only the assigned doctor can view the appointment
    if request.user != appointment.doctor.user:
        return HttpResponseForbidden("You are not authorized to view this appointment.")

    return render(request, "appointment_details.html", {"appointment": appointment})


def view_appointment(request):
    username = request.session.get('username')

    user = get_object_or_404(DoctorReg, username=username)

    try:
        # Get the logged-in doctor
        doctor = DoctorReg.objects.get(username=username)

        # Get only this doctor's Scheduled & Completed appointments
        appo = Appointment.objects.filter(
            Q(status="Scheduled") | Q(status="Completed"),
            doctor=doctor
        ).order_by('-date')

    except DoctorReg.DoesNotExist:
        appo = None  # No appointments, doctor not found

    return render(request, 'Doctor/view_appointment.html', {"appo": appo})

def appointment_completed(request, id):
    req = get_object_or_404(Appointment, id=id)
    req.status = "Completed"  # Fix: Use lowercase 'status' if it's the actual field name
    req.save()
    return HttpResponse("<script>alert('Completed..');window.location='/Doctor/appointments';</script>")


def appointment_cancel(request, id):
    req = get_object_or_404(Appointment, id=id)
    req.status = "Cancelled"  # Fix: Use lowercase 'status' if it's the actual field name
    req.save()
    return HttpResponse("<script>alert('Cancelled..');window.location='/Doctor/appointments';</script>")



def prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)  # Fetch the appointment object
    patient_name = appointment.patient_name.Name  # Get the patient's name
    doctor_name = appointment.doctor.D_name  # Get the doctor's name

    if request.method == "POST":
        form = EPrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient_name = appointment.patient_name  # Assign full patient object to prescription
            prescription.doctor = appointment.doctor  # Automatically assign the doctor from the appointment
            prescription.save()
            return redirect('prescription_success')  # Redirect to a success page or prescriptions list
    else:
        form = EPrescriptionForm(initial={'doctor_name': doctor_name, 'patient_name': patient_name})

    return render(request, 'Doctor/prescription_form.html', {'form': form, 'appointment': appointment})

def view_completed_appointment(request):
    username = request.session.get('username')

    user = get_object_or_404(DoctorReg, username=username)

    try:
        # Get the logged-in doctor
        doctor = DoctorReg.objects.get(username=username)

        # Get only this doctor's Scheduled & Completed appointments
        appo = Appointment.objects.filter(
            Q(status="Completed"),
            doctor=doctor
        ).order_by('-date')

    except DoctorReg.DoesNotExist:
        appo = None  # No appointments, doctor not found
        messages.success(request, "Appointment has been successfully completed.")  # Success message

    return render(request, 'Doctor/appointment_completed.html', {"appo": appo})

def add_medical_record(request, appointment_id):
    # Get the appointment details
    appointment = get_object_or_404(Appointment, id=appointment_id)
    patient = appointment.patient_name  # Fetch patient
    doctor = appointment.doctor  # Fetch doctor

    if request.method == "POST":
        form = PatientMedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient_name = patient  # Assign patient from appointment
            medical_record.doctor_name = doctor  # Assign doctor from appointment
            medical_record.save()
            return redirect('add_medical_record', appointment_id=appointment.id)  # ✅ FIXED: Pass `appointment_id`

    else:
        form = PatientMedicalRecordForm()

    return render(request, 'Doctor/medicalrecord_form.html', {
        'form': form,
        'appointment': appointment,
        'patient': patient,
        'doctor': doctor
    })


def medical_records_list(request, appointment_id):
    # Get the appointment details
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Fetch medical records for this appointment's patient
    medical_records = PatientMedicalRecord.objects.filter(patient_name=appointment.patient_name)

    return render(request, 'Doctor/medical_record_view.html', {
        'medical_records': medical_records,
        'appointment': appointment,
        'patient': appointment.patient_name,  # Pass patient details
        'doctor': appointment.doctor  # Pass doctor details
    })



def delete_medical_record(request, record_id):
    # Fetch the medical record or return 404 if not found
    medical_record = get_object_or_404(PatientMedicalRecord, id=record_id)

    # Get the related appointment ID (assuming it's linked via patient)
    appointment = get_object_or_404(Appointment, patient_name=medical_record.patient_name)

    if request.method == "POST":
        medical_record.delete()
        messages.success(request, "Medical record deleted successfully.")
        return redirect('view_completed_appointment')

    return render(request, 'Doctor/delete_confirmation.html', {'medical_record': medical_record})



def user_logout(request):
    logout(request)
    return redirect('U_home')