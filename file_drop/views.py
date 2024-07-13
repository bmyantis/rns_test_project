from rest_framework import permissions
from drf_rw_serializers import viewsets

from django_filters.rest_framework import DjangoFilterBackend

from .models import FileDrop
from .serializers import FileDropDeserializer, FileDropSerializer
from .filters import FileDropFilter


class FileDropViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FileDropFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return FileDropSerializer
        return FileDropDeserializer

    def get_queryset(self):
        # Retrieve files associated with the current user
        return FileDrop.objects.filter(user=self.request.user)

