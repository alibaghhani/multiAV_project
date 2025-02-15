from types import NoneType

from rest_framework import mixins, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from .models import ScanFile, Scan
from .serializers import ScanFileCreateSerializer, ScanFileRetrieveSerializer, ScanDetailSerializer, ScanListSerializer
from drf_yasg.utils import swagger_auto_schema

class ScanFileViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    model = ScanFile
    serializer_class = ScanFileCreateSerializer
    queryset = ScanFile.objects.all()
    lookup_field = 'sha_256'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ScanFileRetrieveSerializer
        return ScanFileCreateSerializer

    def retrieve(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
            after calculating file's hash if file has status so return file if not return {"status":"queued..."}
        """
        sha_256 = self.kwargs.get(self.lookup_field)

        try:
            obj = self.get_queryset().get(sha_256=sha_256)
            if not isinstance(obj.status, NoneType):
                serializer = self.get_serializer(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"status": "queued..."}, status=status.HTTP_202_ACCEPTED)

        except Exception:
            raise NotFound("object was not found!")




class ScanViewSet(ReadOnlyModelViewSet):

    def get_serializer_class(self):
        """Use different serializers for list and retrieve actions."""
        if self.action == "retrieve":
            return ScanDetailSerializer
        return ScanListSerializer

    def get_queryset(self):
        """Get all scans related to a specific file"""
        sha_256 = self.kwargs.get("file_sha_256")
        return Scan.objects.filter(file__sha_256=sha_256)

    def retrieve(self, request, *args, **kwargs):
        """Get a specific scan by AV name"""
        sha_256 = self.kwargs.get("file_sha_256")
        av_name = kwargs.get("pk")

        try:
            scan = Scan.objects.get(file__sha_256=sha_256, av_name=av_name)
            serializer = self.get_serializer(scan)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Scan.DoesNotExist:
            raise NotFound(f"No scan found for {av_name}")