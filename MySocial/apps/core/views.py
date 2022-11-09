from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


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


# profile Pagination
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
