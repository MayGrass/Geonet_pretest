from rest_framework.routers import DefaultRouter
from apps.views import GeoMetryViewSet

router = DefaultRouter()
router.register("geometry", GeoMetryViewSet, basename="geometry")

urlpatterns = router.urls
