from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.docs import SchemaView
from config import settings

urlpatterns = (
    [
        path("api/v1/", include("apps.core.routes")),
        path("admin/", admin.site.urls),
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

admin.site.site_header = "core Admin"
admin.site.site_title = "core"
admin.site.index_title = "core"
admin.site.site_url = "core"
