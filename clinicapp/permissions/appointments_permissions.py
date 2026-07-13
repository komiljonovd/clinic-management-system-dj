from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role in ['ADMIN','DOCTOR','RECEPTIONIST']:
            return True
        
        if request.user.role == 'PATIENT':
            if obj.patient.user == request.user:
                if request.method in permissions.SAFE_METHODS:
                    return True
                return request.method in ['PATCH', 'PUT','DELETE']
            return False
