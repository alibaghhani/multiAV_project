from core.utilities import get_file_size, calculate_file_hash
from django.conf import settings
from django.db import models


class ScanFileManager(models.Manager):
    def create(self, **kwargs):
        file = kwargs['file']

        kwargs['name'] = str(file)
        kwargs['sha_256'] = calculate_file_hash(file)
        kwargs['file_size'] = file.size

        return super().create(**kwargs)
