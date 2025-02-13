from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ScanFileViewSet, ScanViewSet

router = DefaultRouter()
router.register(r'file', ScanFileViewSet, basename='file')

scan_router = NestedDefaultRouter(router, r'file', lookup='file')
scan_router.register(r'scans', ScanViewSet, basename='file-scans')

urlpatterns = router.urls + scan_router.urls