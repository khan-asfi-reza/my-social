from rest_framework import serializers


class UUIDRelatedField(serializers.SlugRelatedField):
    slug_field = "uuid"

    def __init__(self, **kwargs):
        super().__init__(slug_field=self.slug_field, **kwargs)

    def to_representation(self, obj):
        return str(getattr(obj, self.slug_field))