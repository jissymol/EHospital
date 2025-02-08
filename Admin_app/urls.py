from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('home/', views.home, name='home'),
    path('department/', views.department, name='department'),
    path('doctor_reg/', views.register_doctor, name='doctor_reg'),
    path('success/', views.success_page, name='success_page'),
    path('patient_view/', views.patient_view, name='patient_view'),
    path('deletepatient/<int:user_id>', views.deletepatient, name='deletepatient'),
    path('doctor_view/', views.doctor_view, name='doctor_view'),
    path('deletedoctor/<int:doctor_id>', views.deletedoctor, name='deletedoctor'),
    path('department_view_a/', views.department_view, name='department_view_a'),
    path('deletedepartment/<int:department_id>', views.deletedepartment, name='deletedepartment'),
    path('appointment_view/', views.appointment_view, name='appointment_view'),
    path('logout/', views.user_logout, name='Admin_logout'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



