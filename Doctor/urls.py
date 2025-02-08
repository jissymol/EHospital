
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('home/', views.home, name='Doctorhome'),
    path('create/', views.prescription_create, name='prescription_create'),
    path('schedules/', views.list_schedules, name='list_schedules'),
    path('schedules/create/', views.create_schedule, name='create_schedule'),
    path('schedules/delete/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('doctors/', views.doctors, name='doctors'),
    path('view_department/', views.view_department, name='view_department'),
    path('singleview_department/<int:dep_id>/', views.singleview_department, name='singleview_department'),
    path("appointments/", views.view_appointment, name="view_appointments"),
    path('appointment_completed/<int:id>/', views.appointment_completed, name='appointment_completed'),
    path('appointment_cancel/<int:id>/', views.appointment_cancel, name='appointment_cancel'),
    path('prescription/<int:appointment_id>/', views.prescription, name='prescription'),
    path('view_completed_appointment/', views.view_completed_appointment, name='view_completed_appointment'),
    path('add_medical_record/<int:appointment_id>/', views.add_medical_record, name='add_medical_record'),
    path('medical-records/<int:appointment_id>/', views.medical_records_list, name='medical_records_list'),
    path('delete_medical_record/<int:record_id>/', views.delete_medical_record, name='delete_medical_record'),
    path('logout/', views.user_logout, name='doctor_logout'),

    #path('unauthorized_access/', views.unauthorized_access, name='unauthorized_access'),

]





