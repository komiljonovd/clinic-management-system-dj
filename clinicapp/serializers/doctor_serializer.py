from clinicapp.models import Doctor
from rest_framework import serializers


class DoctorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source ='user.first_name',read_only=True)
    last_name = serializers.CharField(source ='user.last_name',read_only=True)
    email = serializers.CharField(source ='user.email',read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id','user','email','first_name','last_name','speciality','experience','consultation_fee','work_schedule']


    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')

        if request.user.is_authenticated and request.user.role !='ADMIN':
            fields['user'].read_only=True

        return fields
