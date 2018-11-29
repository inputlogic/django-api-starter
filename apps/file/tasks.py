import io

from django.conf import settings
from PIL import Image
import requests
from workers import task

from .libs import upload_to_s3
from .models import File


def _get_destination(file, size):
    path = '/'.join(file.link.split('/')[-2:])
    ext = '.' + path.split('.')[-1]
    return path.replace(ext, '_{0}{1}'.format(size, ext))


@task()
def resize_images():
    """
    Get all images to be resized and push into their own tasks

    """
    images = File.images_to_resize()
    for f in images:
        resize_image(f.id)


@task()
def resize_image(file_id):
    """
    Resize individual image

    """
    file = File.objects.get(pk=file_id)
    res = requests.get(file.link, stream=True)

    if res.status_code >= 300:
        raise Exception('{0}: {1}'.format(res.status_code, res.content))

    im = Image.open(res.raw)

    for size in settings.FILE_IMAGE_SIZES:
        im.resize(size['dimensions'])
        buffer = io.BytesIO()
        im.save(buffer)
        upload_to_s3(buffer, _get_destination(file, size['key']))
