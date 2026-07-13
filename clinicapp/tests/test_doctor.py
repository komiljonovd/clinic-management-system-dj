from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from clinicapp.models import Doctor

User = get_user_model()

class DoctorPermissionTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(email='admin777@gmail.com', role='ADMIN')
        self.receptionist = User.objects.create(email='recepadmin@gmail.com', role='RECEPTIONIST')
        self.doc_user = User.objects.create(email='doctorendlor@gmail.com', role='DOCTOR')
        self.doctor = Doctor.objects.create(user=self.doc_user, speciality='Cardio', consultation_fee=100)
        
        self.list_url = reverse('doctor-list-create')
        self.detail_url = reverse('doctor-detail', kwargs={'user_id': self.doc_user.id})

    def test_receptionist_permissions(self):
        """Receptionist faqat ko'ra olishi kerak (GET)"""
        self.client.force_authenticate(user=self.receptionist)
        
        # GET ruxsat beriladi
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_200_OK)
        
        # POST ruxsat berilmaydi (IsAdminOrReadOnly)
        self.assertEqual(self.client.post(self.list_url, {}).status_code, status.HTTP_403_FORBIDDEN)

    def test_doctor_object_permissions(self):
        """Doktor o'z ma'lumotini tahrirlay olishi kerak, lekin DELETE mumkin emas"""
        self.client.force_authenticate(user=self.doc_user)
        
        # GET (ruxsat)
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        
        # PUT/PATCH (ruxsat)
        self.assertEqual(self.client.patch(self.detail_url, {'speciality': 'New'}).status_code, status.HTTP_200_OK)
        
        # DELETE (taqiqlangan)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_full_access(self):
        """Admin hamma narsani qila oladi"""
        self.client.force_authenticate(user=self.admin)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_204_NO_CONTENT)