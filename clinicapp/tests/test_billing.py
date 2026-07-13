from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from clinicapp.models import Billing, Appointment, Patient, Doctor
from django.utils import timezone
import datetime

User = get_user_model()

class BillingPermissionTests(APITestCase):
    def setUp(self):

        self.admin = User.objects.create(email='admin123@test.com', role='ADMIN')
        self.cashier = User.objects.create(email='cashier234@test.com', role='CASHIER')
        self.pat_user = User.objects.create(email='patsdasd1@test.com', role='PATIENT')
        
        self.patient = Patient.objects.create(user=self.pat_user)
        self.doctor = Doctor.objects.create(user=User.objects.create(email='doc@test.com', role='DOCTOR'), consultation_fee=100)
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, 
            appointment_date=timezone.now() + datetime.timedelta(days=1)
        )
        self.billing = Billing.objects.create(
            appointment=self.appointment, 
            amount=150.00, 
            status='UNPAID'
        )
        
        self.list_url = reverse('billing-list-create')
        self.detail_url = reverse('billing-detail', kwargs={'pk': self.billing.pk})

    def test_finance_roles_access(self):

        self.client.force_authenticate(user=self.cashier)
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.patch(self.detail_url, {'status': 'PAID'}).status_code, status.HTTP_200_OK)

    def test_patient_read_only_access(self):

        self.client.force_authenticate(user=self.pat_user)
        
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        
        self.assertEqual(self.client.patch(self.detail_url, {'status': 'PAID'}).status_code, status.HTTP_403_FORBIDDEN)