from rest_framework_nested import routers
from .views import CategoryViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
app_name = 'catalog'

urlpatterns = router.urls