from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from MySocial.views import UUIDModelViewSet
from .permission import IsPostOrIsAuthenticated
from .serializers import UserSerializer, UserSerializerPublic
from .models import User


class UserCRUDViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet
                      ):
    """
    get: Returns Authenticated User's Details
    post: Creates User
    put: Updates User
    patch: Updates User
    """
    serializer_class = UserSerializer
    permission_classes = [IsPostOrIsAuthenticated]

    def get_object(self):
        """
        Returns Request User / Authenticated User
        """
        return self.request.user

    def get_queryset(self):
        """
        Returns Authenticated User
        """
        return self.request.user

    def list(self, request, *args, **kwargs):
        serialized = self.get_serializer(
            instance=self.get_object()
        )
        return Response(serialized.data)

    def update(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserPublicViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        UUIDModelViewSet
                        ):
    """
    User ViewSet for Public View Only
    """
    serializer_class = UserSerializerPublic
    queryset = User.objects.all()
