from django.urls import path
from rest_framework_nested import routers

from .views import RegisterUserView, UserViewSet

router = routers.DefaultRouter()
router.register(prefix="me", viewset=UserViewSet, basename="me")

app_name = "users"

urlpatterns = [
    *router.urls,
    path("register/", RegisterUserView.as_view(), name="register"),
]
