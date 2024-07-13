from rest_framework.routers import DefaultRouter
from .views import FileDropViewSet

from django.urls import path, include

router = DefaultRouter()

router.register(r'', FileDropViewSet, basename='file_drop')

urlpatterns = [
    path('', include(router.urls)),
]