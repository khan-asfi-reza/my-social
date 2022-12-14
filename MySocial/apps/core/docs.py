from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

class Gen(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        try:
            for definition in schema.definitions.keys():
                if hasattr(
                    schema.definitions[definition]._NP_serializer.Meta,
                    "swagger_example",
                ):
                    examples = schema.definitions[
                        definition
                    ]._NP_serializer.Meta.swagger_example
                    for example in examples.keys():
                        if example in schema.definitions[definition]["properties"]:
                            schema.definitions[definition]["properties"][example][
                                "example"
                            ] = examples[example]
        except AttributeError:
            pass
        return schema


SchemaView = get_schema_view(
    openapi.Info(
        title="core Documentation",
        default_version="v1",
        description="core",
        terms_of_service="https://khanasfireza.dev",
        contact=openapi.Contact(email="info@khanasfireza.dev"),
        license=openapi.License(name="EULA"),
    ),
    permission_classes=[AllowAny],
    generator_class=Gen,
    public=True,
)
