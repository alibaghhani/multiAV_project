from celery import shared_task
from core.utilities import request, get_nested_value
from scanner.models import ScanFile, Scan


@shared_task(serializer='json')
def upload_file_to_av(**kwargs):
    file = ScanFile.objects.get(sha_256=kwargs['file_hash'])

    with open(f'media/{file.file.name}', 'rb') as file:
        response = request(url=kwargs['url'] + kwargs['suffix'],
                                files={'file': file},
                                post=True)

    if response.status_code == 200:
        parsed_response = response.json()
        scan = Scan.objects.get(file=file)
        scan.status = 2
        scan.tracking_id = get_nested_value(parsed_response, kwargs['route'])
        scan.save()
    else:
        raise Exception(f"File upload failed with status code {response.status_code}: {response.text}")




