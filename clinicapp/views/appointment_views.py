from rest_framework import generics,permissions,filters
from clinicapp.serializers.appointments_serializer import Appointment,AppointmentSerializer
from clinicapp.permissions.appointments_permissions import IsAdminOrReadOnly
from .cache import CacheMixin
from django_filters.rest_framework import DjangoFilterBackend



class AppointmentListCreateAPI(CacheMixin,generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    search_fields = ['patient__user__email']
    filterset_fields=['status']
    ordering_fields = ['created_at']


    
    

class AppointmentDetailAPI(CacheMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdminOrReadOnly]

    