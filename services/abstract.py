from abc import ABC, abstractmethod
import requests


class AbstractAntivirus(ABC):

    def __init__(self,
                 file,
                 ):
        self._file = file

    def scan(self):
        self.upload_file()
        if not self._file_id:
            raise ValueError("file id cant be empty")
        self.get_results()

    def request(self, url, files=None, post: bool = False, ):
        """
        handle request based on its type (post/get)

        """
        if post:
            return requests.post(url=url,
                                 files=files,
                                 **self.authenticate())
        else:
            return requests.get(url=url,
                                **self.authenticate())



    @abstractmethod
    def upload_file(self):
        """
        request.post("file").data(data)

        """

    @abstractmethod
    def get_results(self):
        """
        return results.json

        """

    @abstractmethod
    def authenticate(self, **kwargs):
        """
        handle authentication method of each subclass

        """


    @abstractmethod
    def save_report(self,
                    response: dict):
        """
        handles saving reports

        """

