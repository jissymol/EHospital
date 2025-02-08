from django.db import models
from datetime import date

# Create your models here.
class Patient_reg(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    Name = models.CharField(max_length=200)
    Age = models.IntegerField()
    Location = models.CharField(max_length=200)
    District = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    Phone = models.IntegerField()
    Photo = models.ImageField(upload_to='patient_media')
    Date = models.DateField(default=date.today)
    Username = models.CharField(max_length=200)
    password1 = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return str(self.Name)


class Login_user(models.Model):
    Username = models.CharField(max_length=200)
    password1 = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)
    type=models.CharField(max_length=200)

    def __str__(self):
        return str(self.Username)


