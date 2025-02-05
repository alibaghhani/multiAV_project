from core.utilities import calculate_file_hash, get_file_size
from django.conf import settings
from django.db import models


class ScanFileManager(models.Manager):
    def create(self, **kwargs):
        kwargs['name'] = str(kwargs['file'])


        instance = super().create(**kwargs)

        file_path = instance.file.path

        instance.sha_256 = calculate_file_hash(file_path)

        instance.file_size = get_file_size(file_path)

        instance.save(update_fields=['sha_256', 'name', 'file_size'])
        return instance
