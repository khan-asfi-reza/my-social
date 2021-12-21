from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from MySocial import settings
from MySocial.docs import SchemaView

urlpatterns = (
    [
        path("api/v1/", include("MySocial.router")),
        path("admin", admin.site.urls),
        path(
            "api-docs/",
            SchemaView.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            SchemaView.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

admin.site.site_header = "MySocial Admin"
admin.site.site_title = "MySocial"
admin.site.index_title = "MySocial"
admin.site.site_url = "MySocial"
