from django.contrib import admin
from clinicapp.models import Doctor,Patient,Appointment,Prescription,Laboratory,Billing,MedicalRecord

# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user','speciality','experience','consultation_fee','created_at','updated_at']
    search_fields = ['speciality']
    list_display_links = ['user','speciality','experience','consultation_fee']
    list_filter =['experience','created_at','updated_at','speciality']
    ordering = ['-created_at']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user','emergency_contact','medical_history','blood_group','allergies','created_at','updated_at']
    search_fields = ['medical_history','blood_group','allergies','emergency_contact']
    list_display_links = ['user','emergency_contact','medical_history','blood_group',]
    list_filter = ['blood_group','created_at','updated_at']
    ordering = ['-created_at']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient','doctor','appointment_date','status','notes','created_at','updated_at']
    list_display_links = ['patient','doctor','appointment_date','status']
    search_fields = ['notes']
    list_filter = ['status','created_at','updated_at']
    ordering = ['-created_at']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['appointment','diagnosis','medications','treatment_plan','notes','created_at','updated_at']
    list_display_links = ['appointment','diagnosis','medications','treatment_plan']
    search_fields = ['diagnosis','medications','treatment_plan','notes']
    list_filter = ['diagnosis','created_at','updated_at']
    ordering = ['-created_at']


@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ['appointment','upload_result','pdf_report','created_at','updated_at']
    list_filter = ['created_at','updated_at']
    ordering = ['-created_at']


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ['appointment','amount','status','payment_history','created_at','updated_at']
    list_display_links = ['appointment','amount','status','payment_history']
    list_filter = ['status','created_at','updated_at']
    ordering = ['-created_at']
    

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient','diagnosis','analysis','rentgen_file','created_at','updated_at']
    list_display_links = ['patient','diagnosis','analysis']
    list_filter = ['created_at','updated_at']
    ordering = ['-created_at']