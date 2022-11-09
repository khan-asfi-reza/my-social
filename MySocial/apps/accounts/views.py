from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import (CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin,
                                   RetrieveModelMixin)

from .permission import IsPostOrIsAuthenticated
from .serializers import UserSerializer, UserSerializerPublic, UserSerializerPublicDetails
from .models import User
from ..core.views import UUIDGenericViewSet


class UserCRUDViewSet(CreateModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin,
                      ListModelMixin,
                      UUIDGenericViewSet
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
        kwargs.pop('partial', True)
        return super(UserCRUDViewSet, self).update(request, partial=True, *args, **kwargs)


class UserPublicViewSet(RetrieveModelMixin,
                        ListModelMixin,
                        UUIDGenericViewSet
                        ):
    """
    User ViewSet for Public View Only
    """

    serializer_class = UserSerializerPublic
    queryset = User.objects.all()
    # Custom swagger schema settings config for this view
    swagger_schema_settings = {
        "details": {
            "method": "get",
            "responses": {
                200: UserSerializerPublicDetails()
            }
        },
        "list": {
            "responses": {
                200: UserSerializerPublicDetails()
            }
        }
    }

    @action(methods=["get"], detail=True)
    def details(self, request, *args, **kwargs):
        serializer = UserSerializerPublicDetails(
            instance=self.get_object()
        )
        return Response(serializer.data)
