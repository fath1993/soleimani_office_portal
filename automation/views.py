import subprocess
import threading
from django.http import JsonResponse
from automation.tasks import AutomationMainFunctionThread


def start_service_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            AutomationMainFunctionThread(name='automation_main_function_thread').start()
            return JsonResponse({'message': 'service has been started'})
        else:
            return JsonResponse({'message': 'not allowed'})
    else:
        return JsonResponse({'message': 'not allowed'})


def stop_service_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            RestartGunicornThread().start()
            return JsonResponse({'message': 'service has been restarted and not available about 1 minute.'})
        else:
            return JsonResponse({'message': 'not allowed'})
    else:
        return JsonResponse({'message': 'not allowed'})


class RestartGunicornThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        subprocess.run(['sudo', 'systemctl', 'restart', f'gunicorn'], check=False)
