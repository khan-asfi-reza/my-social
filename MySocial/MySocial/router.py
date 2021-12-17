from Accounts.views import UserCRUDViewSet, UserPublicViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()

# Accounts ViewSet
router.register(r"account", UserCRUDViewSet, basename="account")
router.register(r"users", UserPublicViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("Authentication.urls")),
]
