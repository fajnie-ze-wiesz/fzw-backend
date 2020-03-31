from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import setting


class MediaStorage(S3Boto3Storage):
    bucket_name = setting('FZW_MEDIA_S3_BUCKET')
    file_overwrite = False
