from rest_framework import serializers

from MySocial.serializers import UUIDRelatedField
from Profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile Details Serializer
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
    Profile Picture Serializer
    """

    class Meta:
        model = Profile
        fields = ["profile_picture", "online", "last_online"]
        read_only_fields = ["profile_picture", "online", "last_online"]
