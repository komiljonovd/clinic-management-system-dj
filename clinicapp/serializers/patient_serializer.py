from rest_framework import permissions,serializers
from clinicapp.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source = 'user.email')
    first_name =serializers.ReadOnlyField(source = 'user.first_name')
    last_name = serializers.ReadOnlyField(source = 'user.last_name')

    class Meta:

        model = Patient
        fields = ['id','user','email','first_name','last_name','medical_history','blood_group','allergies','emergency_contact']

