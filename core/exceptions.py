class MultiAVExceptions(Exception):
    """
    base exception class for multi AV project
    """


class FileUploadError(MultiAVExceptions):
    """
    exception raises when we have error while uploading a file to av server
    """


class GetFileResultError(MultiAVExceptions):
    """
    exception raises when we have error while getting scan result
    """

