from django.http import JsonResponse

from accounts.custom_decorator import CheckLogin, CheckPermissions, RequireMethod
from gallery.models import delete_file
from utilities.http_metod import fetch_data_from_http_post


class FileGalleryView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='file', allowed_actions='delete')
    @RequireMethod(allowed_method='POST')
    def delete_file(self, request, *args, **kwargs):
        context = {}
        file_id = fetch_data_from_http_post(request, 'file_id', context)
        if delete_file(file_id):
            return JsonResponse({"message": f'فایل با شناسه یکتای {file_id} حذف شد', 'result': 'deleted'})
        else:
            return JsonResponse({"message": f'فایل با شناسه یکتای {file_id} یافت نشد'})

