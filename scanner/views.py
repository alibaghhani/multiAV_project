from types import NoneType
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import ScanFile, Scan
from .serializers import ScanFileCreateSerializer, ScanFileRetrieveSerializer, ScanDetailSerializer, ScanListSerializer
from drf_yasg.utils import swagger_auto_schema

class ScanFileViewSet(ModelViewSet):
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
                return Response(serializer.data)
            else:
                return Response({"status": "queued..."})

        except Exception:
            raise NotFound("object was not found!")


    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('not allowed')

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('not allowed')

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('not allowed')


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
            return Response(serializer.data)
        except Scan.DoesNotExist:
            raise NotFound(f"No scan found for {av_name}")