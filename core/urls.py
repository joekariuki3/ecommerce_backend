from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from apps.catalog import urls as catalog_urls
from apps.users import urls as users_urls
from apps.users.views import LogoutView
from core.views import landing_page

schema_view = get_schema_view(
    openapi.Info(
        title="E-commerce API",
        default_version="v1",
        description="E-commerce API documentation",
        contact=openapi.Contact(email="joelkmuhoho@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", landing_page, name="landing-page"),
    path("admin/", admin.site.urls),
    path("api/users/", include(users_urls, namespace="users")),
    path("api/catalog/", include(catalog_urls, namespace="catalog")),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/auth/logout/", LogoutView.as_view(), name="logout"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
