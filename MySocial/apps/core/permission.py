from rest_framework import permissions


class ProfilePermissionClass(permissions.BasePermission):

    # allow all POST requests
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if (
            request.method == "GET" or request.method == "POST"
        ) and request.user.is_authenticated:
            return True
        elif (
            request.method == "PUT" or request.method == "DELETE"
        ) and request.user.is_authenticated:
            return obj.user == request.user
        return False


class IsAdminOrPostOrGet(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # allow all POST requests
        if request.method == "POST":
            return True

        # Otherwise, only allow authenticated requests

        return (
            (request.user.is_authenticated and request.user == obj.user)
            or request.user.is_admin
            or request.user.is_staff
        )


class IsAuthenticatedOrGet(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # allow all POST requests
        if request.method == "GET":
            return True

        # Otherwise, only allow authenticated requests

        return (
            request.user.is_authenticated
            or request.user.is_admin
            or request.user.is_staff
        )
