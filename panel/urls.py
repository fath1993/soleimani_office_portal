from django.urls import path

from panel.views import DashboardView

app_name = 'panel'

urlpatterns = [
    path('', DashboardView().main, name='panel-dashboard'),
]
