from rest_framework.routers import DefaultRouter
from .views import ScanView



router = DefaultRouter()
router.register(
    'file',
    ScanView,
    'file'
)

urlpatterns = [

] + router.urlsST