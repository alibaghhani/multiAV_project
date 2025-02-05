from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from .models import ScanFile
from .serializers import ScanFileCreateSerializer


class ScanView(ModelViewSet):
    model = ScanFile
    serializer_class = ScanFileCreateSerializer
    queryset = ScanFile.objects.all()



