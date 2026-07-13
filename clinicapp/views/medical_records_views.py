from rest_framework import generics,permissions
from clinicapp.serializers.medical_records_serializer import MedicalRecord,MedicalRecordSerializer
from clinicapp.permissions.medical_records_permissions import IsMedicalRecordsPermission
from .cache import CacheMixin


class MedicalRecordListCreateAPI(CacheMixin,generics.ListCreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated,IsMedicalRecordsPermission]


class MedicalRecordDetailAPI(CacheMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated,IsMedicalRecordsPermission]

