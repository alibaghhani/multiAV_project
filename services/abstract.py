from abc import ABC, abstractmethod
import requests


class AbstractAntivirus(ABC):
    """
    base Antivirus class other antiviruses must be implemented from this class

    abstract methods:
            upload_file
            get_results
            authenticate
            analysis_report

    """


    def request(self, url, files=None, post: bool = False, ):
        """
        handle request to AntiVirus based on its type (post/get)

        """
        if post:
            return requests.post(url=url,
                                 files=files,
                                 **self.authenticate())

        return requests.get(url=url,
                            **self.authenticate())



    @abstractmethod
    def upload_file(self, file):
        """
        upload file to Antivirus
        request.post("file").data(data)

        """

    @abstractmethod
    def get_results(self, tracking_id):
        """
        get result from AntiVirus
        return results.json

        """

    @abstractmethod
    def authenticate(self, **kwargs):
        """
        handle authentication method of each subclass

        """

    @staticmethod
    @abstractmethod
    def analysis_report(response: str):
        """
        parses raw AntiVirus's result
        """
        pass

