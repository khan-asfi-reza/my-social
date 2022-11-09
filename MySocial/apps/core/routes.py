from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.accounts.views import UserCRUDViewSet, UserPublicViewSet
from apps.core.routers import NoLookupRouter
from apps.profile.views import ProfileViewSet

# Default DRF Router
router = DefaultRouter()
# Custom Router for Patch/Put in Details View
no_lookup_router = NoLookupRouter()
# accounts ViewSet
no_lookup_router.register(r"account", UserCRUDViewSet, basename="account")
# User ViewSet
router.register(r"users", UserPublicViewSet, basename="users")
# profile ViewSet
no_lookup_router.register(r"profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(no_lookup_router.urls)),
    path("auth/", include("apps.authentication.urls")),
]
