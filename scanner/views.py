from rest_framework.viewsets import ModelViewSet

from .managers import ScanFileManager
from .models import ScanFile
from .serializers import ScanFileSerializer


class ScanView(ModelViewSet):
    model = ScanFile
    serializer_class = ScanFileSerializer
    queryset = ScanFile.objects.all()



