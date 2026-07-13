from rest_framework import serializers
from clinicapp.models import Laboratory

class LaboratorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Laboratory
        fields = ['id','appointment','upload_result','pdf_report']