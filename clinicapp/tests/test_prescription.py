from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ..models import Prescription, Appointment, Patient, Doctor
from django.utils import timezone
import datetime

User = get_user_model()

class PrescriptionPermissionTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(email='admin123@test.com', role='ADMIN')
        self.doc_user = User.objects.create(email='docasdqev@test.com', role='DOCTOR')
        self.pat_user = User.objects.create(email='patqweqwe@test.com', role='PATIENT')
        
        self.patient = Patient.objects.create(user=self.pat_user)
        self.doctor = Doctor.objects.create(user=self.doc_user,consultation_fee=1500000)
        
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, 
            appointment_date=timezone.now() + datetime.timedelta(days=1)
        )
        self.prescription = Prescription.objects.create(
            appointment=self.appointment, 
            diagnosis="Flu", 
            medications={"dori": "Parasetamol"},
            treatment_plan="Rest",
            notes="Drink water"
        )
        
        self.list_url = reverse('prescription-list-create')
        self.detail_url = reverse('prescription-detail', kwargs={'pk': self.prescription.pk})

    def test_admin_doctor_access(self):

        self.client.force_authenticate(user=self.doc_user)
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_patient_access_logic(self):
        self.client.force_authenticate(user=self.pat_user)
        
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        
        self.assertEqual(self.client.patch(self.detail_url, {'notes': 'Bad note'}).status_code, status.HTTP_403_FORBIDDEN)
        
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)