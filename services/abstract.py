from abc import ABC, abstractmethod
import requests


class AbstractAntivirus(ABC):

    def __init__(self,
                 file_hash,
                 ):

        self._file_hash = file_hash
        self._file_id = None

    def scan(self):
        self.upload_file()
        if not self._file_id:
            raise ValueError("file id cant be empty")
        self.get_results()

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