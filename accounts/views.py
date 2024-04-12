from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import re

from utilities.http_metod import fetch_data_from_http_post


def login_view(request):
    context = {'page_title': 'ورود به حساب کاربری'}
    if request.user.is_authenticated:
        return redirect('panel:panel-dashboard')
    else:
        if request.method == 'POST':
            try:
                username = request.POST['username']
                if username == '':
                    username = None
            except:
                username = None
            if username is None:
                context['err'] = 'نام کاربری بدرستی وارد نشده است'
                return render(request, 'accounts/auth-login-basic.html', context)
            try:
                password = request.POST['password']
                if password == '':
                    password = None
            except:
                password = None
            if password is None:
                context['username'] = username
                context['err'] = 'کلمه عبور بدرستی وارد نشده است'
                return render(request, 'accounts/auth-login-basic.html', context)

            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request=request, user=user)
                return redirect('panel:panel-dashboard')
            else:
                try:
                    user = User.objects.get(username=username)
                    context['username'] = username
                    context['err'] = 'کلمه عبور صحیح نیست'
                    return render(request, 'accounts/auth-login-basic.html', context)
                except:
                    context['username'] = username
                    context['err'] = 'نام کاربری در سامانه وجود ندارد'
                    return render(request, 'accounts/auth-login-basic.html', context)

        return render(request, 'accounts/auth-login-basic.html', context)


def logout_view(request):
    logout(request=request)
    return redirect('accounts:login')


def signup_view(request):
    context = {'page_title': 'ثبت نام کاربر جدید'}
    if request.user.is_authenticated:
        return redirect('panel:panel-dashboard')
    else:
        if request.method == 'POST':
            full_name = fetch_data_from_http_post(request, 'full-name', context)
            if full_name is None:
                context['err'] = 'نام و نام خانوادگی بدرستی وارد نشده است'
                return render(request, 'accounts/auth-register-basic.html', context)
            phone_number = fetch_data_from_http_post(request, 'phone-number', context)
            if phone_number is None:
                context['full_name'] = full_name
                context['err'] = 'شماره همراه بدرستی وارد نشده است'
                return render(request, 'accounts/auth-register-basic.html', context)
            email = fetch_data_from_http_post(request, 'email', context)
            if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
                email = None
            if email is None:
                context['full_name'] = full_name
                context['phone_number'] = phone_number
                context['err'] = 'ایمیل بدرستی وارد نشده است'
                return render(request, 'accounts/auth-register-basic.html', context)
            username = fetch_data_from_http_post(request, 'username', context)
            if username is None:
                context['full_name'] = full_name
                context['phone_number'] = phone_number
                context['email'] = email
                context['err'] = 'نام کاربری بدرستی وارد نشده است'
                return render(request, 'accounts/auth-register-basic.html', context)
            password1 = fetch_data_from_http_post(request, 'password1', context)
            if password1 is None:
                context['full_name'] = full_name
                context['phone_number'] = phone_number
                context['email'] = email
                context['username'] = username
                context['err'] = 'کلمه عبور بدرستی وارد نشده است'
                return render(request, 'accounts/auth-register-basic.html', context)
            password2 = fetch_data_from_http_post(request, 'password2', context)
            if password2 is None:
                context['full_name'] = full_name
                context['phone_number'] = phone_number
                context['email'] = email
                context['username'] = username
                context['err'] = 'تکرار کلمه عبور بدرستی وارد نشده است'
                return render(request, 'accounts/auth-register-basic.html', context)
            if password1 != password2:
                context['full_name'] = full_name
                context['phone_number'] = phone_number
                context['email'] = email
                context['username'] = username
                context['err'] = 'کلمه عبور بدرستی تکرار نشده است'
                return render(request, 'accounts/auth-register-basic.html', context)
            terms = fetch_data_from_http_post(request, 'terms', context)
            if terms is None:
                context['full_name'] = full_name
                context['phone_number'] = phone_number
                context['email'] = email
                context['username'] = username
                context['err'] = 'استفاده از خدمات سایت بدون تایید قوانین امکان پذیر نیست'
                return render(request, 'accounts/auth-register-basic.html', context)

            try:
                user = User.objects.get(username=username)
                context['full_name'] = full_name
                context['phone_number'] = phone_number
                context['email'] = email
                context['username'] = username
                context['err'] = 'نام کاربری از قبل در سامانه وجود دارد'
                return render(request, 'accounts/auth-register-basic.html', context)
            except:
                user = User.objects.create(username=username, first_name=full_name,
                                           email=email)
                user.set_password(password1)
                user.save()
                profile = user.user_profile
                profile.mobile_phone_number = phone_number
                profile.save()
                login(request=request, user=user)
                return redirect('panel:panel-dashboard')

        return render(request, 'accounts/auth-register-basic.html', context)
