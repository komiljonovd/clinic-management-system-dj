from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from clinicapp.models import MedicalRecord, Patient
from django.utils import timezone

User = get_user_model()

class MedicalRecordPermissionTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(email='admin123@test.com', role='ADMIN')
        self.doc_user = User.objects.create(email='doctorend@test.com', role='DOCTOR')
        self.pat_user = User.objects.create(email='patthend12@test.com', role='PATIENT')
        
        self.patient = Patient.objects.create(user=self.pat_user)
        self.record = MedicalRecord.objects.create(
            patient=self.patient,
            diagnosis="Common Cold",
            analysis="Clear",
            treatment_history="Rest"
        )
        
        self.list_url = reverse('medical-record-list-create')
        self.detail_url = reverse('medical-record-detail', kwargs={'pk': self.record.pk})

    def test_admin_doctor_access(self):
        """Admin va Doktor to'liq huquqqa ega"""
        self.client.force_authenticate(user=self.doc_user)
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_200_OK)
        # Doktor tahrirlay oladi
        self.assertEqual(self.client.patch(self.detail_url, {'diagnosis': 'Flu'}).status_code, status.HTTP_200_OK)

    def test_patient_access_restricted(self):
        """Bemor faqat o'zini ko'ra oladi, tahrirlay olmaydi"""
        self.client.force_authenticate(user=self.pat_user)
        
        # GET - OK
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        
        # PATCH - Forbidden
        self.assertEqual(self.client.patch(self.detail_url, {'diagnosis': 'Fake'}).status_code, status.HTTP_403_FORBIDDEN)
        
        # DELETE - Forbidden
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)