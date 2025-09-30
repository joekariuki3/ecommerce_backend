from django.urls import path
from rest_framework_nested import routers

from .views import RegisterUserView, UserViewSet

router = routers.DefaultRouter()
router.register(prefix="", viewset=UserViewSet, basename="user")

app_name = "users"

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    *router.urls,
]
