from rest_framework.test import force_authenticate
from model_bakery import baker

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from file_drop.views import FileDropViewSet
from file_drop.models import FileDrop
from file_drop.serializers import FileDropDeserializer, FileDropSerializer

User = get_user_model()


class VendorViewSetTest(TestCase):
    """
    Test cases for FileDropViewSet using Django TestCase.
    """

    def setUp(self):
        """
        Set up initial data and state for each test case.
        """
        self.view = FileDropViewSet
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user_with_empty_data = User.objects.create_user(username='testuser2', email='test2@example.com', password='testpassword')

        # Create a test FileDrop
        self.fileDrop2 = baker.make(FileDrop, file_name='test 2', user=self.user)
        self.fileDrop1 = baker.make(FileDrop, file_name='test 1', user=self.user)

    def test_get_serializer_class_list_retrieve(self):
        """
        Test get_serializer_class method for list and retrieve actions.
        """
        viewset = FileDropViewSet()
        viewset.action = 'list'
        self.assertEqual(viewset.get_serializer_class(), FileDropSerializer)

    def test_get_serializer_class_other_actions(self):
        """
        Test get_serializer_class method for other actions (not list or retrieve).
        """
        viewset = FileDropViewSet()
        viewset.action = 'create'
        self.assertEqual(viewset.get_serializer_class(), FileDropDeserializer)

    def test_get_queryset(self):
        """
        Test get_queryset method to ensure correct filtering by user.
        """
        view = self.view()
        request = self.factory.get('/api/file_drop/')
        request.user = self.user
        view.request = request

        expected = [self.fileDrop1.id, self.fileDrop2.id]
        actual = view.get_queryset()

        self.assertQuerysetEqual(actual, expected, lambda item: item.id, ordered=False)

    def test_file_drop_list(self):
        """
        Test list endpoint to ensure it returns expected data for authenticated user.
        """
        view = self.view.as_view({'get': 'list'})
        request = self.factory.get('/api/file_drop/')
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([str(self.fileDrop2.id), str(self.fileDrop1.id)], [filedrop['id'] for filedrop in response.data])

    def test_file_drop_list_with_empty_data(self):
        """
        Test list endpoint when user has no associated data.
        """
        view = self.view.as_view({'get': 'list'})
        request = self.factory.get('/api/file_drop/')
        force_authenticate(request, user=self.user_with_empty_data)
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.data)

    def test_file_drop_create(self):
        """
        Test create endpoint to ensure new FileDrop objects can be created.
        """
        view = self.view.as_view({'post': 'create'})
        # Prepare mock file data
        file_content = b'This is a mock file content.'
        file = SimpleUploadedFile('test_file.txt', file_content, content_type='text/plain')

        data = {'file': file}
        request = self.factory.post('/api/file_drop/', data=data, format='multipart')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FileDrop.objects.count(), 3)
