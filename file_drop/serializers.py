import base64

import boto3
from io import BytesIO
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers
from cryptography.fernet import Fernet

from django.conf import settings

from .models import FileDrop
from .helper.validators import validate_file_format


class FileDropDeserializer(serializers.ModelSerializer):
    """Deserializer for FileDrop model."""

    id = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field='file_drop.FileDrop.id'),
        read_only=True
    )
    file = serializers.FileField(validators=[validate_file_format])

    class Meta:
        model = FileDrop
        fields = ('id', 'file')

    def create(self, validated_data):
        # Explicitly set the user to the current user
        user = self.context['request'].user
        # Get uploaded file
        uploaded_file = validated_data.pop('file')
        file_name = uploaded_file.name

        key = settings.ENCRYPTION_KEY
        # Decode the base64-encoded key
        decoded_key = base64.urlsafe_b64decode(key.encode())
        cipher_suite = Fernet(decoded_key)

        # Encrypt the file content
        encrypted_data = cipher_suite.encrypt(uploaded_file.read())

        # Upload encrypted file to AWS S3
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            # Define the full S3 key including the media prefix
            s3_key = f"{settings.AWS_STORAGE_BUCKET_SUBDIRECTORY_NAME}/{file_name}"

            # Wrap encrypted data in BytesIO for upload
            encrypted_file_obj = BytesIO(encrypted_data)
            encrypted_file_obj.seek(0)

            s3.upload_fileobj(
                encrypted_file_obj,
                settings.AWS_STORAGE_BUCKET_NAME,
                s3_key,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': uploaded_file.content_type
                }
            )

            # Save file information in the database
            file_upload = FileDrop.objects.create(
                user=user,
                file_name=file_name,
                file=file_name,
            )
            return file_upload

        except Exception as e:
            raise serializers.ValidationError(f'Error uploading file: {e}')


class FileDropSerializer(serializers.ModelSerializer):
    """Serializer for FileDrop model."""
    id = serializers.PrimaryKeyRelatedField(pk_field=HashidSerializerCharField(source_field='file_drop.FileDrop.id'),
                                            read_only=True)

    class Meta:
        model = FileDrop
        fields = ('id', 'file_name', 'file')

    def __str__(self):
        return self.file_name
