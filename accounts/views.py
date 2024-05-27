from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
import re

from django.urls import reverse

from accounts.custom_decorator import CheckPermissions, CheckLogin, RequireMethod
from accounts.models import Role
from accounts.serializer import ProfileSerializer
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


class ProfileView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست کاربران', 'get_params': request.GET.urlencode()}

        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست کاربران شامل *{search}*', 'get_params': request.GET.urlencode()}

            q = Q()
            if search:
                q &= (
                        Q(**{'username': search}) |
                        Q(**{'user_profile__first_name__icontains': search}) |
                        Q(**{'user_profile__last_name__icontains': search}) |
                        Q(**{'user_profile__role__title': search})
                )

        users = User.objects.filter().order_by('id')
        context['users'] = users

        items_per_page = 50
        paginator = Paginator(users, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'accounts/profiles/user-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='read')
    def detail(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'اطلاعات کاربر *{user.username}*',
                       'user': user, 'get_params': request.GET.urlencode()}
            return render(request, 'accounts/profiles/user-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='read')
    @RequireMethod(allowed_method='POST')
    def rest_detail(self, request, *args, **kwargs):
        context = {}
        user_id = fetch_data_from_http_post(request, 'user_id', context)
        try:
            user = User.objects.filter(id=user_id)
            serializer = ProfileSerializer(user, many=True)
            json_response_body = {
                "method": "post",
                "request": f"اطلاعات کاربر با ایدی {user_id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({"message": 'user not found'})

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست کاربران شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'username': search}) |
                    Q(**{'user_profile__first_name__icontains': search}) |
                    Q(**{'user_profile__last_name__icontains': search}) |
                    Q(**{'user_profile__role__title': search})
            )
        users = User.objects.filter(q).order_by('id')
        context['users'] = users

        items_per_page = 50
        paginator = Paginator(users, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'accounts/profiles/user-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت کاربر جدید', 'get_params': request.GET.urlencode()}

        first_name = fetch_data_from_http_post(request, 'first_name', context)
        last_name = fetch_data_from_http_post(request, 'last_name', context)
        national_code = fetch_data_from_http_post(request, 'national_code', context)
        email = fetch_data_from_http_post(request, 'email', context)
        mobile_phone_number = fetch_data_from_http_post(request, 'mobile_phone_number', context)
        landline = fetch_data_from_http_post(request, 'landline', context)
        card_number = fetch_data_from_http_post(request, 'card_number', context)
        isbn = fetch_data_from_http_post(request, 'isbn', context)
        address = fetch_data_from_http_post(request, 'address', context)
        role_id = fetch_data_from_http_post(request, 'role_id', context)
        password1 = fetch_data_from_http_post(request, 'password1', context)
        password2 = fetch_data_from_http_post(request, 'password2', context)

        if not mobile_phone_number:
            context['err'] = 'شماره همراه بدرستی وارد نشده است'
            return render(request, 'accounts/profiles/user-list.html', context)
        if not password1:
            context['err'] = 'رمز عبور بدرستی وارد نشده است'
            return render(request, 'accounts/profiles/user-list.html', context)
        if not password2:
            context['err'] = 'تکرار رمز عبور بدرستی وارد نشده است'
            return render(request, 'accounts/profiles/user-list.html', context)
        if password1 != password2:
            context['err'] = 'رمز عبور و تکرار رمز عبور یکسان نیستند'
            return render(request, 'accounts/profiles/user-list.html', context)

        username = f'{mobile_phone_number}'
        try:
            User.objects.get(username=username)
            context['err'] = 'نام کاربری از قبل موجود است'
        except:
            pass
            new_user = User.objects.create_user(username=username, first_name=f'{first_name}',
                                                last_name=f'{last_name}', email=f'{email}',
                                                password=password1)
            profile = new_user.user_profile
            if first_name:
                profile.first_name = first_name
            if last_name:
                profile.last_name = last_name
            if national_code:
                profile.national_code = national_code
            if mobile_phone_number:
                profile.mobile_phone_number = mobile_phone_number
            if landline:
                profile.landline = landline
            if card_number:
                profile.card_number = card_number
            if isbn:
                profile.isbn = isbn
            if address:
                profile.address = address
            if role_id:
                profile.role_id = Role.objects.get(id=role_id)
            profile.save()
            context['message'] = f'کاربر با نام کاربری {mobile_phone_number} ایجاد گردید'

        return redirect('panel:user-list')

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='modify')
    def modify(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'ویرایش اطلاعات کاربر *{user.username}*',
                       'user': user, 'get_params': request.GET.urlencode()}

            if request.method == 'GET':
                return render(request, 'accounts/profiles/user-edit.html', context)
            else:
                first_name = fetch_data_from_http_post(request, 'first_name', context)
                last_name = fetch_data_from_http_post(request, 'last_name', context)
                national_code = fetch_data_from_http_post(request, 'national_code', context)
                email = fetch_data_from_http_post(request, 'email', context)
                mobile_phone_number = fetch_data_from_http_post(request, 'mobile_phone_number', context)
                landline = fetch_data_from_http_post(request, 'landline', context)
                card_number = fetch_data_from_http_post(request, 'card_number', context)
                isbn = fetch_data_from_http_post(request, 'isbn', context)
                address = fetch_data_from_http_post(request, 'address', context)
                role_id = fetch_data_from_http_post(request, 'role_id', context)
                password1 = fetch_data_from_http_post(request, 'password1', context)
                password2 = fetch_data_from_http_post(request, 'password2', context)

                if password1 and password2:
                    if password1 != password2:
                        context['err'] = 'رمز عبور و تکرار رمز عبور یکسان نیستند'
                        return render(request, 'accounts/profiles/user-list.html', context)
                elif password1 and not password2:
                    context['err'] = 'تکرار رمز عبور بدرستی وارد نشده است'
                    return render(request, 'accounts/profiles/user-list.html', context)
                elif not password1 and password2:
                    context['err'] = 'رمز عبور بدرستی وارد نشده است'
                    return render(request, 'accounts/profiles/user-list.html', context)
                else:
                    pass

                try:
                    user = User.objects.get(username=mobile_phone_number)
                    if email:
                        user.email = email
                    if password1:
                        user.set_password(password1)
                    user.save()
                    profile = user.user_profile
                    if first_name:
                        profile.first_name = first_name
                    if last_name:
                        profile.last_name = last_name
                    if national_code:
                        profile.national_code = national_code
                    if mobile_phone_number:
                        profile.mobile_phone_number = mobile_phone_number
                    if landline:
                        profile.landline = landline
                    if card_number:
                        profile.card_number = card_number
                    if isbn:
                        profile.isbn = isbn
                    if address:
                        profile.address = address
                    if role_id:
                        profile.role_id = Role.objects.get(id=role_id)
                    profile.save()
                    context['message'] = f'کاربر با نام کاربری {mobile_phone_number} ویرایش گردید'
                    return redirect(
                        reverse('panel:user-detail-with-id',
                                kwargs={'user_id': user_id}) + f'?{request.GET.urlencode()}')
                except:
                    return render(request, 'panel/err/err-not-found.html')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='delete')
    def delete(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'حذف کاربر {user.username}', 'get_params': request.GET.urlencode()}
            user.delete()
            return redirect(reverse('panel:user-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')