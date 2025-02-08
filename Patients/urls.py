from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import fill_doctors  # Import the view


urlpatterns = [

    path('home/', views.home,name='D_home'),
    path('department_view/', views.department_view, name='department_view'),
    path('department_singleview/<int:dep_id>/', views.department_singleview, name='department_singleview'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('doctors/', views.doctors_view, name='doctors_view'),
    path('fill_doctors/', fill_doctors, name='fill_doctors'),
    path('doctor_singleview/<int:doc_id>', views.doctor_singleview, name='doctor_singleview'),
    path('appointment_success/', views.appointment_success, name='appointment_success'),
    path('view_completed_appointment/', views.view_completed_appointment, name='view_appointment'),
    path('medical_records_list/', views.medical_records_list, name='medical_records'),
    path('billing/', views.billing_details, name='billing_details'),
    path('payment/', views.process_payment, name='payment'),
    path('logout/', views.user_logout, name='patient_logout'),
    path('health_tips/', views.health_tips, name='health_tips'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)