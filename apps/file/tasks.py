from workers import task

from .models import File


@task()
def resize_images():
    images = File.images_to_resize()
    for f in images:
        resize_image(f.id)


@task()
def resize_image(file_id):
    pass
