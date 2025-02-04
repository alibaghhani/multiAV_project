import hashlib
import io
from pathlib import Path


def calculate_file_hash(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        file_obj = io.BytesIO(file.read())
        hash_ = hashlib.file_digest(file_obj, 'sha256').hexdigest()
    return hash_



def get_file_size(file_path: str)->int:
    return Path(file_path).stat().st_size