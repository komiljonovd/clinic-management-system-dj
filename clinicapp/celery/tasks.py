from celery import shared_task
from django.core.mail import send_mail
from clinicapp.models import Appointment
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_instant_notification(appointment_id):
    """Signal orqali chaqiriladi: CONFIRMED bo'lganda darhol ketadi."""
    app = Appointment.objects.get(id=appointment_id)
    send_mail(
        subject="Appointment Confirmed",
        message="Your appointment is confirmed.",
        from_email='noreply@clinic.uz',
        recipient_list=[app.patient.user.email],
        fail_silently=False,
    )

@shared_task
def send_reminder_notification(appointment_id):
    """Bu vazifa email jo'natadi VA bayroqni yangilaydi."""
    try:
        app = Appointment.objects.get(id=appointment_id)
        
        send_mail(
            subject="Reminder: Appointment Soon",
            message="Your appointment starts in 1 hour.",
            from_email='noreply@clinic.uz',
            recipient_list=[app.patient.user.email],
            fail_silently=False,
        )
        

        Appointment.objects.filter(pk=appointment_id).update(is_reminded=True)
        
        print(f"DEBUG: Appointment {appointment_id} is_reminded set to True.")
        return True
        
    except Appointment.DoesNotExist:
        return "Appointment not found"

@shared_task
def check_upcoming_appointments():
    """Budilnik: Har 5 daqiqada tekshiradi."""
    now = timezone.now()
    threshold = now + timedelta(minutes=60)
    
    appointments = Appointment.objects.filter(
        status='CONFIRMED',
        is_reminded=False,
        appointment_date__range=(now, threshold)
    )
    
    for app in appointments:
        send_reminder_notification.delay(app.id)
        print('Appointment is reminded :',app.id)