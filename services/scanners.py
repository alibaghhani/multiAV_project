import json

from services.abstract import AbstractAntivirus
import requests


class VirusTotal(AbstractAntivirus):
    UPLOAD_URL = 'https://www.virustotal.com/api/v3/files'
    RESULTS_URL = 'https://www.virustotal.com/api/v3/files/'
    CONTENT_TYPE = 'multipart/form-data'

    def upload_file(self):

        response = requests.post(
            self.UPLOAD_URL,
            files={'file': self._file},
            headers=self.set_header()
        )

        if response.status_code == 200:
            parsed_response = response.json()
            self._file_id = parsed_response['data']['id']
            print(f"Uploaded file ID: {self._file_id}")
        else:
            raise Exception(f"File upload failed with status code {response.status_code}: {response.text}")

    def get_results(self):

        if not self._file_id:
            raise ValueError("File ID is not set, cannot fetch results.")

        response = requests.get(
            self.RESULTS_URL + self._file_id,
            headers=self.set_header()
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get results with status code {response.status_code}: {response.text}")



class Kaspersky(AbstractAntivirus):
    UPLOAD_URL = 'https://opentip.kaspersky.com/api/v1/scan/file'
    RESULTS_URL = 'https://opentip.kaspersky.com/api/v1/scan/file'
    CONTENT_TYPE = 'application/octet-stream'

    def upload_file(self):
        return requests.post(
            url=self.UPLOAD_URL + f'?filename={self._file.__name__}',
            headers=self.set_header(),
            data=self._file
        ).text

    def get_results(self,
                    file_id=None):
        return requests.get(self.RESULTS_URL + f'/{file_id}',
                            headers=self.set_header()).json()