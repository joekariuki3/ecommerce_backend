from rest_framework_nested import routers

from .views import CategoryViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")
app_name = "catalog"

urlpatterns = router.urls
