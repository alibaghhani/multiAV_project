from abc import ABC, abstractmethod
from distutils.dir_util import remove_tree
from typing import Type
from decouple import config
from django.core.files import File


class AbstractAntivirus(ABC):
    UPLOAD_URL = None
    RESULTS_URL = None
    HEADER_KEY_NAME = 'x-api-key'
    CONTENT_TYPE = None

    def __init__(self,
                 file: Type[File],
                 ):

        self._file = file
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
