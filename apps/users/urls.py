from django.urls import path
from .views import RegisterUserView, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('me', UserViewSet)

urlpatterns = [
    *router.urls,
    path('register/', RegisterUserView.as_view(), name='register'),
]