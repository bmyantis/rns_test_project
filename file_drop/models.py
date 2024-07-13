from hashid_field import HashidAutoField

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage


class S3MediaStorage(S3Boto3Storage):
    location = settings.AWS_STORAGE_BUCKET_SUBDIRECTORY_NAME


class FileDrop(models.Model):
    id = HashidAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file = models.FileField(storage=S3MediaStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
