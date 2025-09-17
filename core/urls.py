from django.contrib import admin
from django.urls import path, include
from apps.users import urls as users_urls
from apps.catalog import urls as catalog_urls
from apps.users.views import LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include(users_urls, namespace="users")),
    path("api/catalog/", include(catalog_urls, namespace="catalog")),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/auth/logout/", LogoutView.as_view(), name="logout"),
]
