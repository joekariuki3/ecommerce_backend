from django.urls import path
from .views import RegisterUserView, UserViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(prefix='me', viewset=UserViewSet, basename='me')

app_name = 'users'

urlpatterns = [
    *router.urls,
    path('register/', RegisterUserView.as_view(), name='register'),
]