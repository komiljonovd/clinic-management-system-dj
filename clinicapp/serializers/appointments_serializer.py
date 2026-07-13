from rest_framework import serializers
from django.utils import timezone
from clinicapp.models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    patient_email = serializers.ReadOnlyField(source ='patient.user.email')
    doctor_email = serializers.ReadOnlyField(source ='doctor.user.email')
    
    patient_full_name =serializers.SerializerMethodField()
    doctor_full_name = serializers.SerializerMethodField()
    

    class Meta:
        model = Appointment
        fields = ['id','patient','patient_email','patient_full_name','doctor','doctor_email','doctor_full_name','appointment_date','status','notes']

    def get_patient_full_name(self,obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}".strip()
            
    def get_doctor_full_name(self,obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}".strip()

    def validate_appointment_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('The date must be set for the future.')
        return value