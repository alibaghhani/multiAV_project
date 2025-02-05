from rest_framework.serializers import ModelSerializer
from .models import ScanFile

class ScanFileSerializer(ModelSerializer):
    class Meta:
        model = ScanFile
        fields = ('file', )


