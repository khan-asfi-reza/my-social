from django.urls import path

from .views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Token Obtain and Refresh
    path("", TokenObtainPairView.as_view(), name="jwt-obtain"),
    path("refresh", TokenRefreshView.as_view(), name="jwt-refresh"),
]
