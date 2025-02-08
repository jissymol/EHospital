from django.contrib import admin
from .models import Department,DoctorReg
# Register your models here.
admin.site.register(Department)


@admin.register(DoctorReg)
class DoctorRegAdmin(admin.ModelAdmin):
    list_display = ('D_name', 'gender', 'email', 'phone', 'department', 'date')
    search_fields = ('D_name', 'email', 'phone')
    list_filter = ('gender', 'department', 'district')