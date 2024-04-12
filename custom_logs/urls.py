from django.urls import path
from custom_logs.views import logs_view, ajax_logs_data

app_name = 'logs'

urlpatterns = [
    path('<str:log_level>/', logs_view, name='logs'),
    path('ajax-logs-data', ajax_logs_data, name='ajax-logs-data'),
]

