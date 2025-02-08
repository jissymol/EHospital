from django.db import models
from Admin_app.models import DoctorReg
from User.models import Patient_reg   # Importing the DoctorReg model
# Importing the DoctorReg model

# Create your models here.
class EPrescription(models.Model):
    # Patient Details
    patient_name = models.ForeignKey(Patient_reg, on_delete=models.CASCADE, related_name="prescription")
    doctor = models.ForeignKey(DoctorReg, on_delete=models.CASCADE, related_name="prescriptions")
    pharmacy_information = models.TextField()

    # Medication Details
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50, help_text="How often to take the medication (e.g., 'Twice a day')")
    notes = models.TextField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription for {self.patient_name} by {self.doctor} - {self.medication_name}"




class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(DoctorReg, on_delete=models.CASCADE, related_name="schedules")  # Link to DoctorReg
    available_date = models.DateField()  # Dates when the doctor is available
    time_slot = models.TimeField()
    time_end_slot = models.TimeField()  # Individual time slots (one per entry)
    # Individual time slots (one per entry)
    special_notes = models.TextField(blank=True, null=True)  # Optional notes

    def __str__(self):
        return f"{self.doctor.D_name} - {self.available_date} at {self.time_slot}"


class PatientMedicalRecord(models.Model):
    patient_name = models.ForeignKey(Patient_reg, on_delete=models.CASCADE, related_name='medical_records')

    doctor_name = models.ForeignKey(DoctorReg, on_delete=models.CASCADE, related_name='medical_records')

    # Medical History
    medical_history = models.TextField(blank=True, null=True)

    # Current Diagnosis
    current_diagnosis = models.TextField(blank=True, null=True)

    # Allergies
    allergies = models.TextField(blank=True, null=True)

    # Medications
    medications = models.TextField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Record for {self.patient_name.Name} by Dr. {self.doctor_name.D_name}"