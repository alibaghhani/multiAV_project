from rest_framework.exceptions import MethodNotAllowed
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import ScanFile
from .serializers import ScanFileCreateSerializer


class ScanView(ModelViewSet):
    model = ScanFile
    serializer_class = ScanFileCreateSerializer
    queryset = ScanFile.objects.all()
    lookup_field = 'sha_256'


    def retrieve(self, request, *args, **kwargs):
        try:
            obj = self.get_queryset().get(sha_256=kwargs['sha_256'])
            if not obj.status:
                return Response({"status": "queued"})
        except ScanFile.DoesNotExist:
            raise NotFound()

        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('not allowed')

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('not allowed')
