from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from clinicapp.models import Laboratory, Appointment, Patient, Doctor
from django.utils import timezone
import datetime
User = get_user_model()

class LaboratoryPermissionTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(email='admin123@test.com', role='ADMIN')
        self.tech = User.objects.create(email='techffdsf@test.com', role='LAB_TECHNICIAN')
        self.doc_user = User.objects.create(email='docrewrwe@test.com', role='DOCTOR')
        self.pat_user = User.objects.create(email='patwerwer@test.com', role='PATIENT')
        
        self.patient = Patient.objects.create(user=self.pat_user)
        self.doctor = Doctor.objects.create(user=self.doc_user, speciality='Gen', consultation_fee=100)
        self.appointment = Appointment.objects.create(patient=self.patient, doctor=self.doctor, appointment_date=timezone.now() + datetime.timedelta(days=1))
        self.lab = Laboratory.objects.create(appointment=self.appointment)
        
        self.list_url = reverse('laboratory-list-create')
        self.detail_url = reverse('laboratory-detail', kwargs={'pk': self.lab.pk})

    def test_technician_access(self):
        self.client.force_authenticate(user=self.tech)
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_204_NO_CONTENT)

    def test_doctor_access(self):
        self.client.force_authenticate(user=self.doc_user)
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.post(self.list_url, {'appointment': self.appointment.id}).status_code, status.HTTP_201_CREATED)

    def test_patient_access(self):
        self.client.force_authenticate(user=self.pat_user)
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)