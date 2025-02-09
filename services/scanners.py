from decouple import config

from scanner.models import ScanFile, Scan
from services.abstract import AbstractAntivirus
from .tasks import upload_file_to_av


class VirusTotal(AbstractAntivirus):
    URL = 'https://www.virustotal.com/api/v3/'

    def upload_file(self):
        upload_file_to_av.apply_async(
            kwargs={"url": self.URL,
                    "file_hash": self._file_hash,
                    "suffix": "file",
                    }
        )

    def get_results(self):

        if not self._file_id:
            raise ValueError("File ID is not set, cannot fetch results.")

        url = self.URL + 'analyses/' + self._file_id
        response = self.request(url=url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get results with status code {response.status_code}: {response.text}")

    def authenticate(self, **kwargs):
        headers = kwargs.get("headers", {})

        headers.update({
            "accept": "application/json",
            "x-apikey": config(self.__class__.__name__)
        })

        kwargs['headers'] = headers

        return kwargs

    def save_report(self,
                    response: dict):

        if response['data']['status'] == 'queued':
            return None

        stats = response["data"]["attributes"]["stats"]

        file_instance = ScanFile.objects.get(file=self._file.name).id
        if stats["malicious"] == 0 and stats["suspicious"] == 0:
            overall_result = 0
        else:
            overall_result = 1

        full_result = response

        Scan.objects.create(file=file_instance,
                            overall_result=overall_result,
                            full_result=full_result)

        return True
