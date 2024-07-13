from io import BytesIO
from unittest.mock import patch

from model_bakery import baker
from rest_framework import serializers
from rest_framework.test import APIRequestFactory, force_authenticate

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from file_drop.models import FileDrop
from file_drop.serializers import FileDropDeserializer

User = get_user_model()

class FileDropDeserializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.factory = APIRequestFactory()

        # Prepare mock file data
        file_content = b'This is a mock file content.'
        file = SimpleUploadedFile('test_file.txt', file_content, content_type='text/plain')
        self.validated_data = {
            'file': file,
        }

    def test_create_method_success(self):
        """
        Test the create method of FileDropDeserializer with valid data.
        """
        # Create a mock request object
        request = self.factory.post('/dummy/', data=self.validated_data, format='multipart')
        request.user = self.user
        force_authenticate(request, user=self.user)

        # Pass the request object in the context to simulate request
        serializer = FileDropDeserializer(context={'request': request}, data=self.validated_data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=self.user)

        # Check if an instance of FileDrop is created
        self.assertIsInstance(instance, FileDrop)

        # Check if the file name matches
        self.assertEqual(instance.file_name, 'test_file.txt')

    @patch('file_drop.serializers.boto3.client')
    def test_create_method_with_s3_upload_failure(self, mock_boto3_client):
        """
        Test the create method of FileDropDeserializer with S3 upload failure.
        """
        # Create a mock request object
        request = self.factory.post('/dummy/', data=self.validated_data, format='multipart')
        request.user = self.user
        force_authenticate(request, user=self.user)

        mock_client = mock_boto3_client.return_value
        mock_client.upload_fileobj.side_effect = Exception("S3 Upload Failed")

        # Pass the request object in the context to simulate request
        serializer = FileDropDeserializer(context={'request': request}, data=self.validated_data)

        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.user)

    def test_create_method_with_invalid_data(self):
        """
        Test the create method of FileDropDeserializer with invalid data.
        """
        invalid_data = {
            'file': 'Invalid file content'  # Invalid file type
        }
        # Create a mock request object
        request = self.factory.post('/dummy/', data=invalid_data, format='json')
        request.user = self.user
        force_authenticate(request, user=self.user)

        # Pass the request object in the context to simulate request
        serializer = FileDropDeserializer(context={'request': request}, data=invalid_data)

        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
