from clinicapp.serializers.doctor_serializer import DoctorSerializer,Doctor
from rest_framework import generics,permissions,filters
from clinicapp.permissions.doctor_permissions import IsDoctorOrReadOnly,IsAdminOrReadOnly
from .cache import CacheMixin



class DoctorListCreateAPI(CacheMixin,generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdminOrReadOnly]   
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['user__email','user__first_name','user__last_name','speciality','experience']
    ordering_fields = ['created_at']
    

class DoctorDetailAPI(CacheMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.select_related('user').all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated,IsDoctorOrReadOnly]
    lookup_field = 'user_id'

    