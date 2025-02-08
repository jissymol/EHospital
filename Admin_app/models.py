from django.db import models
from datetime import date



# Create your models here.
class Department(models.Model):
    Department_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)  # Optional text field for description
    image = models.ImageField(upload_to='department_images/', blank=True, null=True)  # Optional image upload

    def __str__(self):
        return str(self.Department_name)


class DoctorReg(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    D_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    location = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='doctor_media')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=date.today)
    username = models.CharField(max_length=200, unique=True)
    password1 = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)

    def __str__(self):
        return self.D_name