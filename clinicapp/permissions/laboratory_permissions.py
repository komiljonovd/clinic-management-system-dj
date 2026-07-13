from rest_framework import permissions


class IsLaboratoryListPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.user.role in ['ADMIN', 'LAB_TECHNICIAN']:
            return True
        
        if request.user.role in 'DOCTOR':
            if request.method == 'POST':
                return True
            if request.method in permissions.SAFE_METHODS:
                return obj.appointment.doctor.user == request.user
            
        if request.user.role == 'PATIENT':
            if request.method in permissions.SAFE_METHODS:
                return obj.appointment.patient.user == request.user
            
        return False
    

class IsLaboratoryDetailPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.role  == 'PATIENT':
            if request.method in permissions.SAFE_METHODS:
                return obj.appointment.patient.user == request.user
        
        if request.user.role in ['ADMIN','LAB_TECHNICIAN']:
            return True
        
        return False
    



        
