from django.urls import path
from . import pages

urlpatterns = [
    path('file_download/', pages.file_download, name='file_download'),
]
