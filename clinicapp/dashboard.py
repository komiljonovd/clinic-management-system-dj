from django.db.models import Count, Sum
from django.utils import timezone
from django.shortcuts import render
from .models import Appointment, Billing, Doctor
from datetime import timedelta
from django.core.exceptions import PermissionDenied


def dashboard_view(request):

    if not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)):
        raise PermissionDenied
    
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    
    # Ma'lumotlarni yig'ish
    context = {
        'daily_patients': Appointment.objects.filter(appointment_date__date=today).count(),
        
        # related_name='appointments' dan foydalanamiz
        'doctors_load': Doctor.objects.annotate(
            appointment_count=Count('appointments')
        ).order_by('-appointment_count')[:5],
        
        # To'langan pullar
        'total_revenue': Billing.objects.filter(status=Billing.Status.PAID).aggregate(
            total=Sum('amount')
        )['total'] or 0,
        
        'monthly_revenue': Billing.objects.filter(
            status=Billing.Status.PAID, 
            created_at__date__gte=start_of_month
        ).aggregate(total=Sum('amount'))['total'] or 0,
        
        # Prescription modelidan tashxisni olish (to'g'ri bog'lanish)
        'top_diagnoses': Appointment.objects.values('prescription__diagnosis').annotate(
            count=Count('prescription__diagnosis')
        ).exclude(prescription__diagnosis__isnull=True).order_by('-count')[:5]
    }
    
    return render(request, 'clinicapp/dashboard.html', context)