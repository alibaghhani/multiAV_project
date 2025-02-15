from decouple import config

from core.exceptions import FileUploadError, GetFileResultError
from services.abstract import AbstractAntivirus



class VirusTotal(AbstractAntivirus):
    """
    Antivirus class for VirusTotal service all methods were implemented based on VirusTotal docs
    # todo: move host to .env
    """
    URL = 'https://www.virustotal.com/api/v3/'

    def upload_file(self, file):
        response = self.request(url=self.URL + 'files',
                                files={'file': file},
                                post=True)

        if response.status_code == 200:
            parsed_response = response.json()
            tracking_id = parsed_response['data']['id']
            return tracking_id
        else:
            raise FileUploadError(f"File upload failed with status code {response.status_code}: {response.text}")


    def get_results(self, tracking_id):

        if not tracking_id:
            raise ValueError("File ID is not set, cannot fetch results.")

        url = self.URL + 'analyses/' + tracking_id
        response = self.request(url=url)

        if response.status_code == 200:
            return response.json()
        else:
            raise GetFileResultError(f"Failed to get results with status code {response.status_code}: {response.text}")

    def authenticate(self, **kwargs):
        headers = kwargs.get("headers", {})

        headers.update({
            "accept": "application/json",
            "x-apikey": config(self.__class__.__name__)
        })

        kwargs['headers'] = headers

        return kwargs




    @staticmethod
    def analysis_report(response: dict):
        assert isinstance(response, dict), "Response must be a dictionary"
        assert 'data' in response, "'data' key is missing in response"

        data = response['data']
        assert isinstance(data, dict), "data must be a dictionary"

        assert 'status' in data, "status key is missing in the 'data'"
        status = data.get('status')

        if status == 'queued':
            return None

        try:
            attributes = data.get("attributes", {})
            assert isinstance(attributes, dict), "'attributes' must be a dictionary"

            stats = attributes.get("stats", {})


            if stats["malicious"] == 0 and stats["suspicious"] == 0:
                overall_result = 'clean'
            else:
                overall_result = 'infected'

            return overall_result, response

        except KeyError:
            return None
