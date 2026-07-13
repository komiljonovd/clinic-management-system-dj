from rest_framework import permissions

class IsPatientOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.user.role in ['ADMIN','DOCTOR','RECEPTIONIST']:
            return True
        
        return False
    


class IsAdminOrReadOnly(permissions.BasePermission):
        
    def has_object_permission(self, request, view, obj):
                
        if request.user.role in ['ADMIN','DOCTOR','RECEPTIONIST']:
            return True
        
        if request.user.role == 'PATIENT':
            if request.method in permissions.SAFE_METHODS:
                return obj.user == request.user
            return False   
         
        return False