from celery import shared_task
from core.utilities import request, get_nested_value
from scanner.models import ScanFile, Scan
from django.db.models import Q
from django.conf import settings


@shared_task(serializer='json')
def upload_file_to_av(**kwargs):

    with open(settings.MEDIA_ROOT+kwargs['file_name'], 'rb') as file:
        response = request(url=kwargs['url'] + kwargs['suffix'],
                                files={'file': file},
                                post=True)

    if response.status_code == 200:
        scan = Scan.objects.get(Q(file__sha_256=kwargs['file_hash'])|Q(av_name=kwargs['av_name']))
        scan.status = 2
        scan.tracking_id = get_nested_value(response.json(), kwargs['route'])
        scan.save()
    else:
        raise Exception(f"File upload failed with status code {response.status_code}: {response.text}")




