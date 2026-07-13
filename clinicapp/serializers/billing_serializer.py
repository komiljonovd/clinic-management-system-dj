from clinicapp.models import Billing
from rest_framework import serializers

class BillingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Billing
        fields = ['id','appointment','amount','status','payment_history']