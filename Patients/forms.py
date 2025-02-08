from django import forms
from .models import Appointment
from User.models import Patient_reg
from Admin_app.models import  DoctorReg, Department

class AppointmentForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=Patient_reg.objects.all(), empty_label="Select Patient")
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select Department")
    doctor = forms.ModelChoiceField(queryset=DoctorReg.objects.none(), empty_label="Select Doctor")  # Initially empty

    class Meta:
        model = Appointment
        fields = ['patient', 'department', 'doctor', 'date', 'time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['doctor'].queryset = DoctorReg.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass  # Ignore invalid input
        elif self.instance.pk:
            self.fields['doctor'].queryset = self.instance.department.doctorreg_set.all()




