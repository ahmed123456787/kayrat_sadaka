from rest_framework.permissions import BasePermission



class IsMosqueAdmin(BasePermission):
    """Allow mosque admin to create a new staff for the mosque"""
    def has_permission(self, request, view):
        return request.user.is_mosque_admin and request.user.is_authenticated