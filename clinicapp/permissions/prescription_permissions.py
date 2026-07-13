from rest_framework import permissions

class IsPrescriptionListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role in ['ADMIN','DOCTOR']:
            return True
        return False
    

class IsPrescriptionDetailPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['ADMIN','DOCTOR']:
            return True

        if request.user.role == 'PATIENT':
            if request.method in permissions.SAFE_METHODS:
                return obj.appointment.patient.user == request.user
        
        return False

    
