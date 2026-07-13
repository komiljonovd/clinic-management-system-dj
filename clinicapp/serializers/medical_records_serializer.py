from rest_framework import serializers

from clinicapp.models import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalRecord
        fields = ['id','patient','diagnosis','analysis','rentgen_file','treatment_history']