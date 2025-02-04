from django.db import models
from core.utilities import calculate_file_hash, get_file_size
from django.conf import settings
import hashlib
import io



class ScanFileManager(models.Manager):
    def create(self, **kwargs):
        kwargs['sha_256'] = calculate_file_hash(str(kwargs['file']))
        kwargs['name'] = str(kwargs['file'])
        kwargs['file_size'] = get_file_size(settings.MEDIA_ROOT+str(kwargs['file']))
        return super().create(**kwargs)






