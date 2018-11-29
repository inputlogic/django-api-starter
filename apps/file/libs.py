import mimetypes
from uuid import uuid4
import boto3
from botocore.client import Config

from django.conf import settings


def upload_to_s3(file, destination):
    """
    file - A file like object/buffer
    destination - The path to use on S3, can be just filename or path (ex: some/path/image.jpg)

    """
    bucket = settings.AWS_STORAGE_BUCKET_NAME
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_DEFAULT_REGION,
        config=Config(s3={'addressing_style': 'path'})
    )
    return s3.upload_fileobj(file, bucket, destination)


def signed_url(
    file_name,
    file_ext=None,
    file_type=None,
    directory=settings.AWS_LOCATION, # S3_UPLOAD_DIRECTORY,
    bucket=settings.AWS_STORAGE_BUCKET_NAME, # S3_BUCKET,
    key=settings.AWS_ACCESS_KEY_ID, # S3_KEY,
    secret=settings.AWS_SECRET_ACCESS_KEY, # S3_SECRET,
    region=settings.AWS_DEFAULT_REGION, # S3_REGION
    expires_in=3000,
    permissions='public-read'
):
    '''Get a signed url for posting a file to s3.

    Defaults to use settings values:
        AWS_LOCATION
        AWS_STORAGE_BUCKET_NAME
        AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY

    Returns a dict:
        result = {
            'data': dict
            'url': string
            'mime_type': string
        }

    To upload a file:
        - send a post request to result['data']['url']
        - include the following form data:
            - 'file': the file from the file html input
            - each key/value in result['data']['fields']

    Once uploaded, the file will be at result['url']

    reference:
        https://devcenter.heroku.com/articles/s3-upload-python
    '''
    file_type = file_type or mimetypes.guess_type(file_name)[0]
    file_ext = file_ext or file_name.split('.')[-1]
    destination_name = '{0}/{1}.{2}'.format(directory, '{0}_{1}'.format(uuid4().hex, file_name.split('.')[0]), file_ext)
    s3 = boto3.client(
        's3',
        aws_access_key_id=key,
        aws_secret_access_key=secret,
        region_name=region,
        config=Config(s3={'addressing_style': 'path'})
    )

    presigned_post = s3.generate_presigned_post(
        Bucket=bucket,
        Key=destination_name,
        Fields={
            'acl': permissions,
            # 'Content-Type': file_type
        },
        Conditions=[
            {'acl': permissions},
            # {'Content-Type': file_type}
        ],
        ExpiresIn=expires_in
    )

    return {
        'data': presigned_post,
        'url': 'https://{0}.s3.amazonaws.com/{1}'.format(
            bucket,
            destination_name
        ),
        'mime_type': file_type,
    }
