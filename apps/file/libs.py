import logging
import mimetypes
from uuid import uuid4

import boto3
from django.conf import settings


log = logging.getLogger(__name__)


def _client():
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_DEFAULT_REGION,
    )


def _create_file_key(filename):
    """
    Create a key name for upload to s3. This ensures all files uploaded have unique paths

    """
    return '{0}/{1}_{2}'.format(settings.AWS_LOCATION, uuid4().hex, filename)


def _get_file_key(url):
    """
    Gets the file key from a File objects url. Based on the pattern used in `_create_file_key`
    method

    Ex: http://aws.amazon.com/dir/abc123_file.jpg => dir/abc123_file.jpg

    """
    return '/'.join(url.split('/')[-2:])


def upload_file(file, destination, mime_type=None):
    """
    file - A file like object/buffer
    destination - The path to use on S3, can be just filename or path (ex: some/path/image.jpg)

    """
    print('upload---')
    print(file)
    print('to---')
    print(destination)
    resp = _client().upload_fileobj(
        file,
        settings.AWS_STORAGE_BUCKET_NAME,
        destination,
        {'ContentType': mime_type},
    )
    print(resp)
    return resp


def get_upload_url(file_name, acl='private'):
    content_type = mimetypes.guess_type(file_name)[0]
    log.info('acl ' + acl)
    return {
        'url': get_signed_url('put', {
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': _create_file_key(file_name),
            'ContentType': mimetypes.guess_type(file_name)[0],
            'ACL': acl,
        }),
        'content_type': content_type
    }


def get_read_url(file, expires=3600):
    return get_signed_url('get', {
        'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
        'Key': _get_file_key(file.link),
    })


def get_signed_url(method, params):
    if method not in ('put', 'get'):
        raise Exception('invalid signed url method, must be "put" or "get"')
    return _client().generate_presigned_url(method + '_object', params)
