from django.conf import settings
from django.core.files.storage import get_storage_class

from storages.backends.s3boto import S3BotoStorage


class S3StaticStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = settings.AWS_STATIC_STORAGE_BUCKET_NAME
        self.local_storage = get_storage_class(
            'compressor.storage.CompressorFileStorage')()
        super(S3StaticStorage, self).__init__(*args, **kwargs)

    def save(self, name, content):
        name = super(S3StaticStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name


class S3MediaStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = settings.AWS_MEDIA_STORAGE_BUCKET_NAME
        super(S3MediaStorage, self).__init__(*args, **kwargs)


class S3ThumbnailStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = settings.AWS_THUMBNAIL_STORAGE_BUCKET_NAME
        super(S3ThumbnailStorage, self).__init__(*args, **kwargs)


class CachedS3BotoStaticStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = settings.AWS_STATIC_STORAGE_BUCKET_NAME
        super(CachedS3BotoStaticStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            'compressor.storage.CompressorFileStorage')()

    def save(self, name, content):
        self.local_storage._save(name, content)
        super(CachedS3BotoStaticStorage, self).save(
            name, self.local_storage._open(name)
        )
        return name
