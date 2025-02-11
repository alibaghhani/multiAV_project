# Create your models here.
from django.db import models
from core.models import CommonItems
from .managers import ScanFileManager, ScanManager


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

    objects = ScanManager()

    status = models.IntegerField(choices=STATUS_CHOICES)
    av_name = models.CharField(max_length=255)
    file = models.ForeignKey('ScanFile', on_delete=models.CASCADE, related_name='scan')
    tracking_id = models.CharField(max_length=250,null=True)
    short_result = models.IntegerField(choices=CommonItems.RESULT_CHOICES, null=True)
    final_result = models.JSONField(null=True)
    checked_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"Tracking ID: {self.tracking_id}"

