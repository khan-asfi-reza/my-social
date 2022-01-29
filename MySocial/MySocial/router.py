from rest_framework.routers import DefaultRouter, SimpleRouter
from Accounts.views import UserPublicViewSet, UserCRUDViewSet
router = DefaultRouter()

# Accounts ViewSet
router.register(
    r'account',  UserCRUDViewSet, basename='account'
)
router.register(
    r'users',  UserPublicViewSet, basename="users"
)
