from django.http import JsonResponse

from accounts.custom_decorator import CheckLogin, CheckPermissions, RequireMethod
from gallery.models import delete_file


class FileGalleryView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='file', allowed_actions='delete')
    @RequireMethod(allowed_method='POST')
    def delete_file(self, request, file_id, *args, **kwargs):
        if delete_file(file_id):
            return JsonResponse({"message": 'deleted'})
        else:
            return JsonResponse({"message": f'file with id: {file_id} not found.'})

