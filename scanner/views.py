from types import NoneType

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import ScanFile
from .serializers import ScanFileCreateSerializer, ScanFileRetrieveSerializer


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

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('not allowed')

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('not allowed')
