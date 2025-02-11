from datetime import datetime
import ast
from celery import shared_task
from django.conf import settings
from django.db.models import Q
from core.exceptions import FileUploadError, GetFileResultError
from scanner.models import Scan
from .scanners import VirusTotal

RATE_LIMIT_PERIOD_COUNT = getattr(settings, "RATE_LIMIT_PERIOD_COUNT", 2)


@shared_task(serializer='json')
def upload_file_to_virustotal():
    scan_file_objs = Scan.objects.filter(
        Q(status=1)&Q(
        av_name='VirusTotal')).order_by(
        '-checked_at').select_related(
        'file')[:RATE_LIMIT_PERIOD_COUNT]


    for scan_file_obj in scan_file_objs:
        if scan_file_obj.status == 1:
            try:
                with open(settings.MEDIA_ROOT+scan_file_obj.file.file.name, 'rb') as file:
                    vt_obj = VirusTotal()
                    try:
                        tracking_id = vt_obj.upload_file(file)
                        scan_file_obj.tracking_id = tracking_id
                        scan_file_obj.status = 2
                        scan_file_obj.checked_at = datetime.now()
                        scan_file_obj.save()
                    except FileUploadError:
                        continue
            except NotADirectoryError:
                continue
        else:
            break




