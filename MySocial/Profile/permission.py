from rest_framework import permissions


class ProfilePermissionClass(permissions.BasePermission):
    # allow all POST requests
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method == 'GET':
            return True
        elif (request.method == 'PUT' or request.method == 'DELETE') and request.user.is_authenticated:
            return obj.user == request.user
        return False

