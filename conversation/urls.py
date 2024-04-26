from django.urls import path, include

from conversation.views import chat_view

app_name = 'chat'

urlpatterns = [
    path('chat/', chat_view, name='chat'),
]
