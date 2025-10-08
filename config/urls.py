from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
# Swagger uchun schema view
schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="API dokumentatsiyasi",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)

# API routerini yaratish
router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # API URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),  # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),  # Redoc UI (Alternativ Swagger UI)




    ##################################  APP ###########################################
    path("api/v1/lightbulb/", include("app_lightbulb.urls")),
    path("api/v1/heating/", include("app_heating_calc.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)