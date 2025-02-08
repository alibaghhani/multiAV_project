import hashlib
from pathlib import Path

import requests


def calculate_file_hash(uploaded_file)->str:
    hash_obj = hashlib.sha256()

    for chunk in uploaded_file.chunks():
        hash_obj.update(chunk)

    return hash_obj.hexdigest()

def get_file_size(file_path: str) -> int:
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
