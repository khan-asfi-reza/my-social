from rest_framework import serializers

from apps.core.serializers import UUIDRelatedField
from apps.profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    profile Details Serializer
    """
    user = UUIDRelatedField(read_only=True)

    class Meta:
        model = Profile
        exclude = [
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["online", "last_online"]


class ProfilePictureSerializer(serializers.ModelSerializer):
    """
    profile Picture Serializer
    """

    class Meta:
        model = Profile
        fields = ["profile_picture", "online", "last_online"]
        read_only_fields = ["profile_picture", "online", "last_online"]
