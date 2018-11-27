from PIL import Image
import requests
from workers import task

from .models import File


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
    # Open image from url in stream
    # Resize image in memory (bytes)
    # Push resized image (bytes) to s3
    file = File.objects.get(pk=file_id)
    res = requests.get(file.link, stream=True)
    im = Image.open(res.raw)
