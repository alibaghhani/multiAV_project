from core.utilities import calculate_file_hash
from django.conf import settings
from django.db import models
from services.av_settings import AVS


class ScanFileManager(models.Manager):
    def create(self, **kwargs):
        file = kwargs['file']

        kwargs['name'] = str(file)
        kwargs['sha_256'] = calculate_file_hash(file)
        kwargs['file_size'] = file.size

        return super().create(**kwargs)



class ScanManager(models.Manager):


    def bulk_create_scan_for_av_in_avs(self, file_obj):
        data = []
        for av in AVS:
            data.append({'av_name': av.split('.')[2],
                         'status': 1,
                         'file': file_obj})

        instances = [self.model(av_name=data['av_name'],
                          status=data['status'],
                          file=data['file']) for data in data]

        self.model.objects.bulk_create(instances)
