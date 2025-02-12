import ast
from datetime import datetime
from celery import shared_task
from django.conf import settings
from core.exceptions import FileUploadError, GetFileResultError
from .scanners import VirusTotal
from .utils import ScanManager, FileManager


RATE_LIMIT_PERIOD_COUNT = getattr(settings, "RATE_LIMIT_PERIOD_COUNT", 2)


@shared_task(serializer='json')
def upload_file_to_virustotal():
    manager = ScanManager('VirusTotal')
    for scan_obj in manager.get_scan_records(status=1):
        try:
            with open(settings.MEDIA_ROOT + scan_obj.file.file.name, 'rb') as file:
                vt_obj = VirusTotal()
                try:
                    tracking_id = vt_obj.upload_file(file)
                    manager.update_scan_status(scan_obj=scan_obj, tracking_id=tracking_id, status=2,
                                               checked_at=datetime.now())
                except FileUploadError:
                    continue
        except NotADirectoryError:
            continue


@shared_task(serializer='json')
def get_file_scan_result_virustotal():
    manager = ScanManager('VirusTotal')
    file_manager = FileManager()

    for scan_obj in manager.get_scan_records(status=2):
        if scan_obj.status == 2:
            vt_obj = VirusTotal()
            try:
                response = vt_obj.get_results(scan_obj.tracking_id)
                dict_response = ast.literal_eval(response) if isinstance(response, str) else response

                short_result, final_result = vt_obj.analysis_report(dict_response)
                manager.update_scan_status(scan_obj=scan_obj, status=3, short_result=short_result,
                                           final_result=final_result)
                file_manager.save_file_result(scan_obj.file)

            except GetFileResultError:
                continue

        else:
            break