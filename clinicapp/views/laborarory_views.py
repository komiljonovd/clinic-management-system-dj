from rest_framework import generics,permissions
from clinicapp.serializers.laboratory_serializer import Laboratory,LaboratorySerializer
from clinicapp.permissions.laboratory_permissions import IsLaboratoryListPermission,IsLaboratoryDetailPermission
from .cache import CacheMixin


class LaboratoryListCreateAPI(CacheMixin,generics.ListCreateAPIView):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [permissions.IsAuthenticated,IsLaboratoryListPermission]


class LaboratoryDetailAPI(CacheMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [permissions.IsAuthenticated,IsLaboratoryDetailPermission]

    