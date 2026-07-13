from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.cache import cache
from clinicapp.models import (Appointment,Billing,Doctor,
                              Laboratory,MedicalRecord,Patient,Prescription

)
from clinicapp.celery.tasks import send_instant_notification
from django.db import transaction

@receiver([post_save,post_delete],sender=Appointment)
def appointment_del_cache(sender,instance,**kwargs):
    cache.delete_pattern('*AppointmentListCreateAPI*')
    cache.delete_pattern('*AppointmentDetailAPI*')

    if instance.status == 'CONFIRMED':
        send_instant_notification.delay(instance.id)
        print(f"Confirmed 'Appointment' was sent-{instance.id}")



    


@receiver([post_save,post_delete],sender=Billing)
def billing_del_cache(sender,instance,**kwargs):
    cache.delete_pattern('*BillingListCreateAPI*')
    cache.delete_pattern('*BillingDetailAPI*')


@receiver([post_save,post_delete],sender=Doctor)
def doctor_del_cache(sender,instance,**kwargs):
    cache.delete_pattern('*DoctorListCreateAPI*')
    cache.delete_pattern('*DoctorDetailAPI*')


@receiver([post_save,post_delete],sender=Laboratory)
def laboratory_del_cache(sender,instance,**kwargs):
    cache.delete_pattern('*LaboratoryListCreateAPI*')
    cache.delete_pattern('*LaboratoryDetailAPI*')


@receiver([post_save,post_delete],sender=MedicalRecord)
def medical_del_cache(sender,instance,**kwargs):
    cache.delete_pattern('*MedicalRecordListCreateAPI*')
    cache.delete_pattern('*MedicalRecordDetailAPI*')


@receiver([post_save,post_delete],sender=Patient)
def patient_del_cache(sender,instance,**kwargs):
    cache.delete_pattern('*PatientListCreateAPI*')
    cache.delete_pattern('*PatientDetailAPI*')


@receiver([post_save,post_delete],sender=Prescription)
def prescription_del_cache(sender,instance,**kwargs):
    cache.delete_pattern('*PrescriptionListCreateAPI*')
    cache.delete_pattern('*PrescriptionDetailAPI*')











