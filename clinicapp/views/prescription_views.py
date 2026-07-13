from rest_framework import generics,permissions,filters
from clinicapp.serializers.prescription_serializer import Prescription,PrescriptionSerializer
from clinicapp.permissions.prescription_permissions import IsPrescriptionListPermission,IsPrescriptionDetailPermission
from .cache import CacheMixin


class PrescriptionListCreateAPI(CacheMixin,generics.ListCreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated,IsPrescriptionListPermission]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['diagnosis','treatment_plan','notes']
    ordering_fields = ['created_at']


class PrescriptionDetailAPI(CacheMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated,IsPrescriptionDetailPermission]

