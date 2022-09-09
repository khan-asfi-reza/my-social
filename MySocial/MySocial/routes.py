from django.urls import include, path
from rest_framework.routers import DefaultRouter

from Accounts.views import UserCRUDViewSet, UserPublicViewSet
from MySocial.routers import NoLookupRouter
from Profile.views import ProfileViewSet

# Default DRF Router
router = DefaultRouter()
# Custom Router for Patch/Put in Details View
no_lookup_router = NoLookupRouter()
# Accounts ViewSet
no_lookup_router.register(r"account", UserCRUDViewSet, basename="account")
# User ViewSet
router.register(r"users", UserPublicViewSet, basename="users")
# Profile ViewSet
no_lookup_router.register(r"profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(no_lookup_router.urls)),
    path("auth/", include("Authentication.urls")),
]
