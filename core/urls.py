from django.contrib import admin
from django.urls import path, include
from apps.users import urls as users_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include(users_urls))
]
