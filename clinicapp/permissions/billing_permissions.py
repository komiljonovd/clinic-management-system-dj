from rest_framework import permissions

class IsBillingPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role in ['ADMIN','RECEPTIONIST','CASHIER','ACCOUNTANT']:
            return True
        
        if request.user.role == 'PATIENT':
            if request.method in permissions.SAFE_METHODS:
                return obj.appointment.patient.user == request.user
            
        return False
    

