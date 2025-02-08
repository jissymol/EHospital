from django.shortcuts import render
from .models import Login_user,Patient_reg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages,auth
import re


# Create your views here.
def Patientreg(request):
    login_table = Login_user()
    userprofile = Patient_reg()

    if request.method == 'POST':
        Username = request.POST['username']
        Age = request.POST['age']  # Make sure this value is received
        email = request.POST['email']
        Location = request.POST['address']
        District = request.POST['state']
        Phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if Age is provided and valid
        if not Age or not Age.isdigit():
            messages.error(request, 'Please provide a valid age.')
            return render(request, 'User/Patient_reg.html')

        # Check if the username or email already exists
        if Patient_reg.objects.filter(Username=Username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'User/Patient_reg.html')

        if Patient_reg.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered. Please use a different email.')
            return render(request, 'User/Patient_reg.html')

        # Check if the contact number is valid and unique
        if not re.match(r'^\d{10}$', Phone):
            messages.error(request, 'Please enter a valid 10-digit contact number.')
            return render(request, 'User/Patient_reg.html')

        if Patient_reg.objects.filter(Phone=Phone).exists():
            messages.error(request, 'This contact number is already registered.')
            return render(request, 'User/userregister.html')

        # Populate user profile data
        userprofile.Username = Username
        userprofile.Name = request.POST['name']
        userprofile.email = email
        userprofile.Phone = Phone
        userprofile.Age = int(Age)  # Assign age as an integer

        # Check if 'photo' exists in request.FILES
        if 'photo' in request.FILES:
            userprofile.Photo = request.FILES['photo']
        else:
            messages.error(request, 'Please upload a photo.')
            return render(request, 'User/Patient_reg.html')

        userprofile.password1 = password1
        userprofile.password2 = password2

        login_table.Username = Username
        login_table.password1 = password1
        login_table.password2 = password2
        login_table.type = 'patient'

        # Validate passwords match
        if password1 == password2:
            userprofile.save()
            login_table.save()

            messages.success(request, 'Registration successful')
            return redirect('Login')
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'User/Patient_reg.html')

    return render(request, 'User/Patient_reg.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Safely get the username
        password = request.POST.get('password1')  # Safely get the password


        user = Login_user.objects.filter(Username=username, password1=password, type='patient').exists()
        try:
            if user is not None:
                user_details = Login_user.objects.get(Username=username, password1=password)
                user_name = user_details.Username
                user_type = user_details.type

                if user_type == 'patient':
                    request.session['username'] = user_name
                    return redirect('/Patients/home')

                elif user_type == 'doctor':
                    request.session['username'] = user_name
                    return redirect('/Doctor/home')

                elif user_type == 'admin':
                    request.session['username'] = user_name
                    return redirect('/Admin_app/home')

            else:
                messages.error(request, 'Invalid username or password.')

        except:
                messages.error(request, 'An error occurred: ')

    else:
            messages.error(request, 'Username and password are required.')


    return render(request, 'User/Login.html')


def home(request):
    return render(request,'User/home.html')