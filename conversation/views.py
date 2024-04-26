from django.shortcuts import render


def chat_view(request):
    return render(request, 'panel/chat/app-chat.html')
