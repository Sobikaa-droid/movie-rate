from rest_framework.permissions import BasePermission


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsStaffUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return True
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.is_staff
