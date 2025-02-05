from rest_framework.routers import DefaultRouter
from .views import ScanView



router = DefaultRouter()
router.register(
    'scan',
    ScanView,
    'scan'
)

urlpatterns = [

] + router.urls