from django import forms
from .models import EPrescription,PatientMedicalRecord


class EPrescriptionForm(forms.ModelForm):
    doctor_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'style': 'font-weight: bold; font-size: 18px; color: #333;'}),
        required=False
    )

    class Meta:
        model = EPrescription
        fields = ['medication_name', 'dosage', 'frequency', 'pharmacy_information', 'notes']

        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medication Name'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dosage'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Frequency'}),
            'pharmacy_information': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pharmacy'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes'}),
        }



class PatientMedicalRecordForm(forms.ModelForm):
    class Meta:
        model = PatientMedicalRecord
        fields = ['medical_history', 'current_diagnosis', 'allergies', 'medications']
