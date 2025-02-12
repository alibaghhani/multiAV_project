from dataclasses import dataclass, field

from django.conf import settings
from django.db.models import Q

from scanner.models import Scan


@dataclass
class ScanManager:
    av_name: str

    RATE_LIMIT_PERIOD_COUNT: int = field(
        default=getattr(settings, "RATE_LIMIT_PERIOD_COUNT", 2),
        init=False,
        repr=False)

    def get_scan_records(self, status):
        return Scan.objects.filter(
            Q(status=status) & Q(av_name=self.av_name)
        ).order_by('-checked_at').select_related('file')[:self.RATE_LIMIT_PERIOD_COUNT]

    @staticmethod
    def update_scan_status(scan_obj, **kwargs):
        """Update the scan object status, tracking_id, and results if available."""
        for key, value in kwargs.items():
            setattr(scan_obj, key, value)

        scan_obj.save()



class FileManager:

    @staticmethod
    def collect_results(file_obj):
        scans = file_obj.scan.all()

        if scans.count() == settings.COUNT_OF_SCANNERS:
            return list(scans.values_list('short_result', flat=True))

        return None

    def save_file_result(self, file_obj):
        file_obj.status = 'infected' if 'infected' in self.collect_results(file_obj) else 'clean'
        file_obj.save()