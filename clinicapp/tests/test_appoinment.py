from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from clinicapp.models import Appointment, Patient, Doctor
from django.utils import timezone
import datetime

User = get_user_model()

class AppointmentPermissionTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(email='admin123@test.com', role='ADMIN')
        self.pat_user = User.objects.create(email='patawwfd@test.com', role='PATIENT')
        self.doc_user = User.objects.create(email='docrqdsa@test.com', role='DOCTOR')
        
        self.patient = Patient.objects.create(user=self.pat_user)
        self.doctor = Doctor.objects.create(user=self.doc_user,consultation_fee=150000)
        
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now() + datetime.timedelta(days=1),
            status='PENDING'
                )
        
        self.list_url = reverse('appointment-list-create')
        self.detail_url = reverse('appointment-detail', kwargs={'pk': self.appointment.pk})

    def test_admin_full_access(self):
        """Admin har qanday operatsiyani bajara oladi"""
        self.client.force_authenticate(user=self.admin)
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_204_NO_CONTENT)

    def test_patient_access_logic(self):
        self.client.force_authenticate(user=self.pat_user)
        
        response_get = self.client.get(self.detail_url)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
               
        response_patch = self.client.patch(self.detail_url, {'notes': 'Changed note'})
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK) 
        
        response_del = self.client.delete(self.detail_url)
        self.assertEqual(response_del.status_code, status.HTTP_204_NO_CONTENT)