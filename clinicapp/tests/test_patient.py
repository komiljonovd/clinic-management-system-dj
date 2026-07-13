from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from clinicapp.models import Patient

User = get_user_model()

class PatientPermissionTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(email='admin123@test.com', role='ADMIN')
        self.doc = User.objects.create(email='docsdad@test.com', role='DOCTOR')
        self.pat_user = User.objects.create(email='patient1@test.com', role='PATIENT')
        self.other_pat = User.objects.create(email='patient2@test.com', role='PATIENT')
        self.patient = Patient.objects.create(user=self.pat_user, blood_group='A+')
        self.other_patient = Patient.objects.create(user=self.other_pat, blood_group='B+')
        self.list_url = reverse('patient-list-create')
        self.detail_url = reverse('patient-detail', kwargs={'user_id': self.pat_user.id})

    def test_admin_access(self):  
        self.client.force_authenticate(user=self.admin)
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_200_OK)
        response = self.client.patch(self.detail_url, {'blood_group': 'O+'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patient_access_logic(self):
        self.client.force_authenticate(user=self.pat_user)
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.patch(self.detail_url, {'blood_group': 'B+'}).status_code, status.HTTP_403_FORBIDDEN)