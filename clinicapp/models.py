from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.

User = get_user_model()


class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='doctors')
    speciality = models.CharField(max_length=256)
    experience = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    work_schedule = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.speciality}'
    
    
    class Meta:
        db_table ='doctors'
        verbose_name ='doctor'
        verbose_name_plural ='doctors'


class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='patients')
    medical_history = models.TextField(null=True,blank=True)
    blood_group = models.CharField(max_length=20,null=True,blank=True)
    allergies = models.TextField(null=True,blank=True)
    emergency_contact = models.CharField(max_length=256,help_text='001234567 <-- Input in this way' )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name().strip()}" or f"{self.user.email.strip()}"
    
    class Meta:
        db_table ='patients'
        verbose_name ='patient'
        verbose_name_plural ='patients'
    

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')       
        CONFIRMED = 'CONFIRMED', _('Confirmed') 
        COMPLETED = 'COMPLETED', _('Completed') 
        CANCELLED = 'CANCELLED', _('Cancelled')     

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True, null=True)
    is_reminded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.user.email}-{self.doctor.user.email}:{self.appointment_date}"
    
    class Meta:
        db_table ='appointments'
        verbose_name ='appointment'
        verbose_name_plural ='appointments'
        ordering = ['-created_at']


class Prescription(models.Model):
    appointment = models.OneToOneField(
        'Appointment', 
        on_delete=models.CASCADE, 
        related_name='prescription',
    )
    diagnosis = models.TextField()
    medications = models.JSONField(help_text='{"dori": "Parasetamol", "doza": "500mg", "qabul_vaqti": "kuniga 3 mahal"}') 
    treatment_plan = models.TextField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Retsept: {self.appointment.patient} - {self.appointment.doctor.user.get_full_name()}"
    
    class Meta:
        db_table ='prescriptions'
        verbose_name ='prescription'
        verbose_name_plural ='prescriptions'
        ordering = ['-created_at']



class Laboratory(models.Model):
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE)
    upload_result = models.FileField(upload_to='upload_result/',null=True,blank=True)
    pdf_report = models.FileField(upload_to='pdf_report/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Doctor-{self.appointment.doctor.user.email} Patient-{self.appointment.patient.user.email}"
    
    class Meta:
        db_table = 'laboratories'
        verbose_name = 'laboratory'
        verbose_name_plural ='laboratories'
        ordering = ['-created_at']




class Billing(models.Model):
    class Status(models.TextChoices):
        UNPAID = 'UNPAID', 'Unpaid'
        PAID = 'PAID', 'Paid'
        PARTIAL = 'PARTIAL', 'Partial Paid'

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UNPAID)
    payment_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.appointment}-{self.status}" 

    class Meta:
        db_table ='billings'
        verbose_name ='billing'
        verbose_name_plural ='billings'
        ordering = ['-created_at']



class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    analysis = models.TextField()
    rentgen_file = models.FileField(upload_to='records/', blank=True)
    treatment_history = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Patient-{self.patient.user.email}"
    

    class Meta:
        db_table='medical records'
        verbose_name='medical record'
        verbose_name_plural='medical records'
        ordering = ['-created_at']







