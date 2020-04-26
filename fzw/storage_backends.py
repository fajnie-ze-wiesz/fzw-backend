from storages.backends.s3boto3 import S3Boto3Storage  # type: ignore
from storages.utils import setting  # type: ignore


# get_accessed_time, get_created_time, path is not defined but also not used
class MediaStorage(S3Boto3Storage):  # pylint: disable=abstract-method
    bucket_name = setting('FZW_MEDIA_S3_BUCKET')
    custom_domain = setting('FZW_MEDIA_CLOUDFRONT_DOMAIN')
    file_overwrite = False
