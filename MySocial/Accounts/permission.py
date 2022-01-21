from rest_framework import permissions


class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        # Allow Only Create
        if request.method == 'POST':
            return True

        # Otherwise, only allow authenticated requests

        return request.user.is_authenticated


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff


class IsDeleteOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_admin or request.user.is_staff
        else:
            return True
