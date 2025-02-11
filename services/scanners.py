from decouple import config
from core.exceptions import FileUploadError
from scanner.models import ScanFile, Scan
from services.abstract import AbstractAntivirus



class VirusTotal(AbstractAntivirus):
    URL = 'https://www.virustotal.com/api/v3/'

    def upload_file(self):

        response = self.request(url=self.URL + 'files',
                                files={'file': self._file},
                                post=True)

        if response.status_code == 200:
            parsed_response = response.json()
            tracking_id = parsed_response['data']['id']
            return tracking_id
        else:
            raise FileUploadError(f"File upload failed with status code {response.status_code}: {response.text}")


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
