from rest_framework import serializers,permissions
from clinicapp.models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = ['id','appointment','diagnosis','medications','treatment_plan','notes']