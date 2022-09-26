from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
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


class UUIDGenericViewSet(viewsets.GenericViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class UUIDModelViewSet(ModelViewSet, UUIDGenericViewSet):
    """
    UUID Related Field Models ViewSet
    """
