from django.db import models

# Create your models here.
from django.db import models

from core.models import CommonItems


class ScanFile(CommonItems):
    file = models.FileField()
    sha_256 = models.CharField(max_length=64, unique=True)
    file_size = models.BigIntegerField()
    status = models.IntegerField(choices=CommonItems.RESULT_CHOICES)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.sha_256}-----{self.name}'

