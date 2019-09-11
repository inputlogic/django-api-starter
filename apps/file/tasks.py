import io

from django.conf import settings
from PIL import Image
import requests
from workers import task

from .libs import upload_file, get_read_url
from .models import File


def _get_size(image, width):
    """
    Determines the new image width/height based on given image dimensions and a new width

    """
    width_percent = width / float(image.size[0])
    height = float(image.size[1]) * width_percent
    return (width, height)


def _mime_to_format(mime_type):
    """
    This is specific to PIL to ensure we use the right format name

    """
    if mime_type in ('image/jpeg', 'image/jpg'):
        return 'JPEG'

    if mime_type == 'image/png':
        return 'PNG'

    raise Exception('unsupported image mime type: {0}'.format(mime_type))


def _get_destination(file, size):
    path = '/'.join(file.link.split('/')[-2:])
    ext = '.' + path.split('.')[-1]
    return path.replace(ext, '_{0}{1}'.format(size, ext))


# @task(schedule=settings.FILE_IMAGE_RESIZE_SCHEDULE)
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
    file_url = get_read_url(file)
    res = requests.get(file_url, stream=True)

    if res.status_code >= 300:
        raise Exception('{0}: {1}'.format(res.status_code, res.content))

    orig = Image.open(res.raw)

    for size in settings.FILE_IMAGE_SIZES:
        im = orig.copy()
        im.thumbnail(_get_size(im, size['width']), Image.ANTIALIAS)
        buffer = io.BytesIO()
        im.save(buffer, format=_mime_to_format(file.mime_type))
        buffer.seek(0)
        upload_file(buffer, _get_destination(file, size['key']), mime_type=file.mime_type)

    file.verified = True
    file.is_resized = True
    file.save()
