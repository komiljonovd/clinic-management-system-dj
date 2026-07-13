from rest_framework import permissions



class IsAdminOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):

        if request.user.role == 'RECEPTIONIST' and request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'ADMIN'
    

class IsDoctorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.role =='ADMIN':
            return True
        
        if request.user.role =='RECEPTIONIST':
            return request.method in permissions.SAFE_METHODS
        
        return request.user.is_authenticated
    

    def has_object_permission(self, request, view, obj):

        if request.user.role == 'ADMIN' or request.user.role =='RECEPTIONIST':
            return True
        
        if request.user.role == 'DOCTOR':
            if request.method == 'DELETE':
                return False
            return obj.user == request.user
        
        return False
    

