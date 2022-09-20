from rest_framework.decorators import action

from MySocial.views import UUIDModelViewSet
from Profile.permission import ProfilePermissionClass
from Profile.models import Profile
from Profile.serializers import ProfileSerializer


class ProfileViewSet(UUIDModelViewSet):
    """
    Profile View Set to update Profile Details and View Profile Data
    retrieve:
        `tags`: Get Quotes
        `tags`:
            200: ProfileSerializer
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related("user")
    permission_classes = [
        ProfilePermissionClass
    ]
    http_method_names = ["get", "put", "patch"]

    def get_object(self):
        return self.request.user.profile
