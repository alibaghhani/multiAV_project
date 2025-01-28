from services.abstract import AbstractAntivirus
from services.av_settings import AVS
import importlib
from typing import Type
from django.core.files import File


def import_scanners(name: str,
                    path: str)->AbstractAntivirus:

    module = importlib.import_module(path)
    return getattr(module,
                   name)