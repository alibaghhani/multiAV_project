import ast
from datetime import datetime
from celery import shared_task
from django.conf import settings
from core.exceptions import FileUploadError, GetFileResultError
from .scanners import VirusTotal
from .utils import ScanHelper, FileHelper
from core.enums import  STATUS

RATE_LIMIT_PERIOD_COUNT = getattr(settings, "RATE_LIMIT_PERIOD_COUNT", 2)


@shared_task(serializer='json',  rate_limit='1/m')
def upload_file_to_virustotal():
    """
    task uploads file to target scanner
    this action may take some time
    so files must be on a queue to upload

    """
    helper = ScanHelper('VirusTotal')
    for scan_obj in helper.get_scan_records(status=STATUS.NOT_UPLOADED.value):
        try:
            with open(settings.MEDIA_ROOT + scan_obj.file.file.name, 'rb') as file:
                vt_obj = VirusTotal()
                try:
                    tracking_id = vt_obj.upload_file(file)
                    helper.update_scan_status(scan_obj=scan_obj, tracking_id=tracking_id, status=STATUS.PENDING.value,
                                               checked_at=datetime.now())
                except FileUploadError:
                    continue
        except NotADirectoryError:
            continue


@shared_task(serializer='json',  rate_limit='1/m')
def get_file_scan_result_virustotal():
    """
    task get file's results from target scanner
    this action may take some time
    so files must be on a queue to upload

    """
    scan_helper = ScanHelper('VirusTotal')
    file_helper = FileHelper()

    for scan_obj in scan_helper.get_scan_records(status=STATUS.PENDING.value):
        vt_obj = VirusTotal()
        try:
            response = vt_obj.get_results(scan_obj.tracking_id)
            dict_response = ast.literal_eval(response) if isinstance(response, str) else response
            try:
                short_result, final_result = vt_obj.analysis_report(dict_response)
                scan_helper.update_scan_status(scan_obj=scan_obj, status=STATUS.SCANNED.value, short_result=short_result,
                                           final_result=final_result)
                file_helper.save_file_result(scan_obj.file)
            except (ValueError, KeyError):
                continue

        except GetFileResultError:
            continue

