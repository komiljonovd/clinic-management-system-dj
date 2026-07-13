from clinicapp.serializers.patient_serializer import Patient,PatientSerializer
from rest_framework import generics,permissions,filters
from clinicapp.permissions.patient_permissions import IsAdminOrReadOnly,IsPatientOrReadOnly
from .cache import CacheMixin

class PatientListCreateAPI(CacheMixin,generics.ListCreateAPIView):
    queryset = Patient.objects.select_related('user').all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated,IsPatientOrReadOnly]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['user__email','user__first_name','user__last_name']
    ordering_fields = ['created_at']

    
class PatientDetailAPI(CacheMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.select_related('user').all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdminOrReadOnly]
    lookup_field = 'user_id'

    

