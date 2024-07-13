import django_filters

from .models import FileDrop


class FileDropFilter(django_filters.FilterSet):
    file_name = django_filters.CharFilter(field_name='file_name', lookup_expr='icontains')

    class Meta:
        model = FileDrop
        fields = ['file_name', ]
