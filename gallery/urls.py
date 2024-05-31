from django.urls import path
from gallery.views import FileGalleryView

app_name = 'file-gallery'

urlpatterns = [
    path('file/delete-file/', FileGalleryView().delete_file, name='delete-file'),
]
