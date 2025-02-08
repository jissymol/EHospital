
from django import forms
from .models import Department,DoctorReg

class Department_form(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['Department_name', 'description', 'image']
        labels = {
            'Department_name': 'Department Name',
            'description': 'Description',
            'image': 'Department Image',
        }
        widgets = {
            'Department_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class DoctorRegForm(forms.ModelForm):
    class Meta:
        model = DoctorReg
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


