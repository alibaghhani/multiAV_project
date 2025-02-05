from django.db import models

# Create your models here.
from django.db import models

from core.utilities import get_file_size, calculate_file_hash
from .managers import ScanFileManager
from core.models import CommonItems


class ScanFile(CommonItems):
    file = models.FileField()
    sha_256 = models.CharField(max_length=64, null=True, blank=True)
    file_size = models.BigIntegerField( null=True, blank=True)
    status = models.IntegerField(choices=CommonItems.RESULT_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    objects = ScanFileManager()

    def __str__(self):
        return f'{self.sha_256}-----{self.name}'

class Scan(CommonItems):

    STATUS_CHOICES = (
        (1, 'NOT_UPLOADED'),
        (2, 'PENDING'),
        (3, 'SCANNED'),
        (4, 'NOTIFIED')
    )


    status = models.IntegerField(choices=STATUS_CHOICES)
    av_name = models.CharField(max_length=255, unique=True)
    file = models.ForeignKey('ScanFile', on_delete=models.CASCADE, related_name='scan')
    tracking_id = models.BigIntegerField()
    short_result = models.IntegerField(choices=CommonItems.RESULT_CHOICES)
    final_result = models.JSONField()

    def __str__(self):
        return f"Tracking ID: {self.tracking_id}"

