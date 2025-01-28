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


def get_scanners()->list:
    scanners = []
    for scanner in AVS:

        module_name, class_name = scanner.rsplit('.', 1)

        instance = import_scanners(
            name=class_name,
            path=module_name
        )
        scanners.append(instance)

    return scanners

def scan(file: Type[File]):
    for scanner in get_scanners():
        scanner(file=file).scan()
