from django.urls import path, include

from automation.views import start_service_view, stop_service_view

app_name = 'automation'

urlpatterns = [
    path('start/', start_service_view, name='start'),
    path('stop/', stop_service_view, name='stop'),
]
