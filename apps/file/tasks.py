import io
import mimetypes

import requests
from PIL import Image as PImage
from django.conf import settings
from django.core.files.storage import default_storage
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


def _get_name(file_obj, size):
    name = file_obj.s3_object_key.replace(settings.AWS_STORAGE_BUCKET_NAME, '')
    if name[0] == '/':
        name = name[1:]
    parts = name.split('.')
    ext = parts[-1]
    name = parts[0]
    return '{}_{}.{}'.format(name, size, ext)


# @task(schedule=settings.FILE_IMAGE_RESIZE_SCHEDULE)
def resize_images():
    """
    Get all images to be resized and push into their own tasks
    """
    images = File.objects.filter(
        mime_type__in=File.IMAGE_MIME_TYPES,
        is_resized=False,
        is_private=False
    ).all()
    [resize_image(img.id) for img in images]


@task()
def resize_image(file_id):
    file_obj = File.objects.get(pk=file_id)
    orig = PImage.open(file_obj.link)

    for size in settings.FILE_IMAGE_SIZES:
        mem = io.BytesIO()
        img = orig.copy()

        img.thumbnail(_get_size(img, size['width']), PImage.ANTIALIAS)
        img.save(mem,
                 format=_mime_to_format(file_obj.mime_type),
                 quality=size.get('quality', 95))

        mem.seek(0)
        default_storage.save(_get_name(file_obj, size['key']), mem)

        mem.close()
        img.close()

    file.verified = True
    file.is_resized = True
    file.save()
