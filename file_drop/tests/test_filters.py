from model_bakery import baker

from django.test import TestCase
from django_filters import CharFilter
from django.contrib.auth import get_user_model

from file_drop.filters import FileDropFilter
from file_drop.models import FileDrop

User = get_user_model()


class FileDropFilterTestCase(TestCase):
    def setUp(self):
        # Create a test FileDrop
        self.fileDrop2 = baker.make(FileDrop, file_name='test 2')
        self.fileDrop1 = baker.make(FileDrop, file_name='test 1')

    def test_filter_fields(self):

        # Initialize the filter with data
        filter_data = {'file_name': self.fileDrop1.file_name}
        filter_set = FileDropFilter(data=filter_data, queryset=FileDrop.objects.all())

        # Check if filter set is valid
        self.assertTrue(filter_set.is_valid())

        # Check if expected filters are present
        self.assertIsInstance(filter_set.filters['file_name'], CharFilter)

        # Check if filtering works as expected
        filtered_queryset = filter_set.qs
        self.assertEqual(filtered_queryset.count(), 1)
