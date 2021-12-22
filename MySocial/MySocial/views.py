from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from MySocial.permission import ProfilePermissionClass


# General Pagination, 6 content each request
class GeneralPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 6


# Image Pagination
class ImagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10


# Profile Pagination
class ProfilePagination(PageNumberPagination):
    page_size = 11
    page_size_query_param = "page_size"
    max_page_size = 11


class InboxMessagePagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


# Custom Model View Set
class ModelViewSetAttribute(viewsets.ModelViewSet):
    # Token Based Auth
    authentication_classes = [TokenAuthentication]
    # Profile permission
    permission_classes = [IsAuthenticated, ProfilePermissionClass]
    lookup_field = "pk"
    pagination_class = GeneralPagination
    create_serializer_class = None
    model = None

    def get_create_serializer(self, **kwargs):
        return self.create_serializer_class(context={"request": self.request}, **kwargs)


class ListCreateView(ModelViewSetAttribute):
    @action(methods=["post"], detail=False)
    def create(self, request, *args, **kwargs):
        serializer = self.get_create_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(user=request.user)
            retrieve_serializer = self.get_serializer(instance)
            return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDestroyView(ModelViewSetAttribute):
    @action(methods=["put"], detail=False)
    def update(self, request, *args, **kwargs):
        instance = self.model.objects.get(user=request.user)
        serializer = self.get_create_serializer(
            instance=instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            instance = serializer.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UUIDModelViewSet(viewsets.GenericViewSet):
    lookup_field = "uuid"
