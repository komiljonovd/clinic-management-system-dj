from clinicapp.serializers.billing_serializer import Billing,BillingSerializer
from rest_framework import generics,permissions,filters
from clinicapp.permissions.billing_permissions import IsBillingPermission
from .cache import CacheMixin
from django_filters.rest_framework import DjangoFilterBackend



class BillingListCreateAPI(CacheMixin,generics.ListCreateAPIView):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = [permissions.IsAuthenticated,IsBillingPermission]
    filter_backends =[DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at']



class BillingDetailAPI(CacheMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = [permissions.IsAuthenticated,IsBillingPermission]

    
