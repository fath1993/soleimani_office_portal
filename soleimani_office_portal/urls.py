from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('panel.urls')),
    path('accounts/', include('accounts.urls')),
    path('automation/', include('automation.urls')),
    path('gallary/', include('gallery.urls')),
    path('resources/', include('resource.urls')),
    path('reports/', include('reports.urls')),
    path('tickets/', include('tickets.urls')),
    path('webhook/', include('webhook.urls')),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)