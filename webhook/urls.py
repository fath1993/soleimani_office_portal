from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from webhook.views import WebhookView

app_name = 'webhook'

urlpatterns = [
    # Webhook
    path('webhook-request/', csrf_exempt(WebhookView().webhook_request), name='webhook-request'),
]
