from apps.core.views import UUIDModelViewSet
from apps.profile.permission import ProfilePermissionClass
from apps.profile.models import Profile
from apps.profile.serializers import ProfileSerializer


class ProfileViewSet(UUIDModelViewSet):
    """
    profile View Set to update profile Details and View profile Data
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
