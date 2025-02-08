import hashlib
from pathlib import Path
from functools import reduce
import requests


def calculate_file_hash(uploaded_file) -> str:
    """

    :param uploaded_file:
    :return:
        file hash
    """

    hash_obj = hashlib.sha256()

    for chunk in uploaded_file.chunks():
        hash_obj.update(chunk)

    return hash_obj.hexdigest()


def get_file_size(file_path: str) -> int:
    """

    :param file_path:
    :return:
        file size
    """
    return Path(file_path).stat().st_size


def request(url, files=None, post: bool = False, **kwargs):
    """
    handle request based on its type (post/get)

    """
    if post:
        return requests.post(url=url,
                             files=files,
                             **kwargs)

    return requests.get(url=url,
                        **kwargs)



def get_nested_value(data, route):
    """Access nested dictionary value dynamically using dot notation."""
    keys = route.split('.')
    try:
        return reduce(lambda d, key: d[key], keys, data)
    except (KeyError, TypeError):
        return None