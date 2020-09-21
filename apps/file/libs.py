import mimetypes
from uuid import uuid4

import boto3
from django.conf import settings


def delete_from_s3(
    object_key,
    bucket=settings.AWS_STORAGE_BUCKET_NAME,
    key=settings.AWS_ACCESS_KEY_ID,
    secret=settings.AWS_SECRET_ACCESS_KEY,
):
    s3 = boto3.client(
        's3',
        aws_access_key_id=key,
        aws_secret_access_key=secret
    )
    return s3.delete_object(Bucket=bucket, Key=object_key)


def signed_url(
    file_name=None,
    content_type='image/jpeg',
    directory=settings.AWS_LOCATION,
    bucket=settings.AWS_STORAGE_BUCKET_NAME,
    key=settings.AWS_ACCESS_KEY_ID,
    secret=settings.AWS_SECRET_ACCESS_KEY,
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
    content_type = content_type or mimetypes.guess_type(file_name)[0]
    file_ext = file_name.split('.')[-1]
    file_name = uuid4().hex if file_name is None else file_name
    if file_name.endswith(file_ext):
        ext_len = len(file_ext) + 1
        file_name = file_name[:-ext_len]

    destination_name = '{0}/{1}.{2}'.format(directory, file_name, file_ext)
    s3 = boto3.client(
        's3',
        aws_access_key_id=key,
        aws_secret_access_key=secret
    )

    presigned_post = s3.generate_presigned_post(
        Bucket=bucket,
        Key=destination_name,
        Fields={'acl': permissions, 'Content-Type': content_type},
        Conditions=[
            {'acl': permissions},
            {'Content-Type': content_type}
        ],
        ExpiresIn=expires_in
    )

    return {
        'data': presigned_post,
        'url': 'https://{}.s3.amazonaws.com/{}'.format(
            bucket,
            destination_name
        )
    }
