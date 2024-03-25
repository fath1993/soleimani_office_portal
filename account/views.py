from django.contrib.auth import authenticate, logout, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from account.models import Profile
from account.serializer import ProfileSerializer
from utilities.http_metod import fetch_data_from_http_post
from utilities.utilities import create_json


def login_view(request):
    context = {}
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'account/login.html', context)
        else:
            username = fetch_data_from_http_post(request, 'username', context)
            password = fetch_data_from_http_post(request, 'password', context)

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('website:landing')
            else:
                context['err'] = 'user not found'
                return render(request, 'account/login.html', context)
    else:
        return redirect('website:landing')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('accounts:login')


class Account(APIView):
    # authentication_classes = (TokenAuthentication,)
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'profile'}

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user)
        if profile.count() == 0:
            return JsonResponse(
                create_json('post', 'profile', 'failed', f'profile not found'))
        serializer = ProfileSerializer(profile, many=True)
        result_data = serializer.data
        for data in result_data:
            data['email'] = request.user.email
        json_response_body = {
            'method': 'post',
            'request': 'profile',
            'result': 'success',
            'data': result_data,
        }
        return JsonResponse(json_response_body)

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user)
        if profile.count() == 0:
            return JsonResponse(
                create_json('post', 'profile', 'failed', f'profile not found'))
        serializer = ProfileSerializer(profile, many=True)
        result_data = serializer.data
        for data in result_data:
            data['email'] = request.user.email
        json_response_body = {
            'method': 'post',
            'request': 'profile',
            'result': 'success',
            'data': result_data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


