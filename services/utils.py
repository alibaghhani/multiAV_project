from dataclasses import dataclass, field

from django.conf import settings
from django.db.models import Q

from scanner.models import Scan


@dataclass
class ScanManager:
    """
    ScanManager class handles database interactions related to scans.

    It provides methods to retrieve scan records based on the antivirus name
    (av_name) and update the status of scan records efficiently.

    Attributes:
        av_name (str): The name of the antivirus scanner.
        RATE_LIMIT_PERIOD_COUNT (int): The rate limit for retrieving scan records,
                                        defaulting to the value specified in
                                        Django settings.
    """
    av_name: str

    RATE_LIMIT_PERIOD_COUNT: int = field(
        default=getattr(settings, "RATE_LIMIT_PERIOD_COUNT", 2),
        init=False,  # This field is not included during initialization
        repr=False  # This field is not included in the representation string
    )

    def get_scan_records(self, status):
        """
        Retrieve the latest scan records for the specified antivirus scanner
        with a given status.

        Args:
            status (str): The status of the scans to filter (e.g., "completed",
                          "pending", etc.).

        Returns:
            QuerySet: A queryset containing the filtered scan records,
                       ordered by the `checked_at` timestamp, limited
                       by RATE_LIMIT_PERIOD_COUNT.
        """
        return Scan.objects.filter(
            Q(status=status) & Q(av_name=self.av_name)  # Filter by status and av_name
        ).order_by('-checked_at').select_related('file')[:self.RATE_LIMIT_PERIOD_COUNT]

    @staticmethod
    def update_scan_status(scan_obj, **kwargs):
        """
        Update the attributes of a given scan object with new values.

        This method updates the scan object dynamically based on the provided
        keyword arguments and then saves the changes to the database.

        Args:
            scan_obj (Scan): The scan object to be updated.
            **kwargs: Arbitrary keyword arguments representing the fields
                      to update, and their new values.

        Raises:
            AttributeError: If a key in kwargs does not match an attribute
                            of scan_obj.
        """
        for key, value in kwargs.items():
            setattr(scan_obj, key, value)  # Set each provided attribute

        scan_obj.save()  # Save the updated scan object


class FileManager:
    """
    FileManager class handles database interactions related to files.

    It provides methods to collect scan results for files and to save
    the overall result of scans associated with a given file.
    """

    @staticmethod
    def collect_results(file_obj):
        """
        Collect and return the scan results for a given file object.

        If the number of scans for the file matches the expected count
        of scanners as specified in the settings, the method returns
        the short results of the scans. If not, it returns None.

        Args:
            file_obj (File): The file object containing associated scans.

        Returns:
            list or None: A list of short results from the scans, or None
                           if the count does not match the expected count
                           of scanners.
        """
        scans = file_obj.scan.all()  # Retrieve all scan records related to the file

        if scans.count() == settings.COUNT_OF_SCANNERS:
            return list(scans.values_list('short_result', flat=True))  # Return results if the count matches

        return None  # Count does not match; no results to return

    def save_file_result(self, file_obj):
        """
        Save the overall scan result for a given file object.

        This method determines if the file is 'infected' based on the
        scan results collected. It updates the file object's status
        accordingly, and then saves the changes.

        Args:
            file_obj (File): The file object whose status is to be updated.

        Note:
            It is assumed that the `collect_results` method has been
            called to obtain the current scan results before this method is used.
        """
        file_obj.status = 'infected' if 'infected' in self.collect_results(file_obj) else 'clean'
        file_obj.save()  # Save the updated status of the file object