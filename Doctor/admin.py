from django.contrib import admin
from .models import EPrescription,DoctorSchedule


# Register your models here.
@admin.register(EPrescription)
class EPrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'medication_name', 'dosage', 'frequency', 'created_at')
    search_fields = ('patient_name', 'medication_name')



@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'available_date', 'time_slot','time_end_slot', 'special_notes')
    list_filter = ('available_date', 'doctor')
    search_fields = ('doctor__D_name', 'special_notes')
