from django.db import models
from django.db import models
from datetime import date
from Admin_app.models import Department, DoctorReg
from User.models import Patient_reg

# Create your models here.
class Appointment(models.Model):
    # Existing fields
    patient_name = models.ForeignKey(Patient_reg, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorReg, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    reason_for_visit = models.TextField(blank=True, null=True)

    # Appointment Status
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.D_name} ({self.status})"


class PatientBilling(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Insurance', 'Insurance'),
        ('Online', 'Online Payment'),
    ]

    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]

    patient = models.ForeignKey(Patient_reg, on_delete=models.CASCADE, related_name='billing_records')
    billing_id = models.CharField(max_length=20, unique=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    insurance_details = models.TextField(blank=True, null=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Billing {self.billing_id} - {self.patient.Name} ({self.payment_status})"
