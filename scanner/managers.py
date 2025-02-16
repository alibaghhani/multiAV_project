from core.utilities import calculate_file_hash
from django.db import models
from django.conf import settings
from core.enums import STATUS


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
        for av in settings.AVS:
            data.append({'av_name': av.split('.')[2],
                         'status': STATUS.NOT_UPLOADED.value,
                         'file': file_obj})

        instances = [self.model(av_name=data_item['av_name'],
                          status=data_item['status'],
                          file=data_item['file']) for data_item in data]

        self.model.objects.bulk_create(instances)
