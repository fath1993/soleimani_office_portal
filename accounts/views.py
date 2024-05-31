from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
import re

from django.urls import reverse

from accounts.custom_decorator import CheckPermissions, CheckLogin, RequireMethod
from accounts.models import Role, Profile, DeliveryProfile, WarehouseProfile, SellerProfile
from accounts.serializer import ProfileSerializer, SellerProfileSerializer, WarehouseProfileSerializer, \
    DeliveryProfileSerializer
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
    def profile_detail(self, request, *args, **kwargs):
        context = {}
        user_id = fetch_data_from_http_post(request, 'user_id', context)
        try:
            profile = Profile.objects.filter(user__id=user_id)
            serializer = ProfileSerializer(profile, many=True)
            json_response_body = {
                "method": "post",
                "request": f"اطلاعات پروفایل کاربر با ایدی {user_id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({"message": 'user not found'})

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='read')
    @RequireMethod(allowed_method='POST')
    def seller_profile_detail(self, request, *args, **kwargs):
        context = {}
        user_id = fetch_data_from_http_post(request, 'user_id', context)
        try:
            profile = SellerProfile.objects.filter(profile__user__id=user_id)
            serializer = SellerProfileSerializer(profile, many=True)
            json_response_body = {
                "method": "post",
                "request": f"اطلاعات پروفایل فروشندگی کاربر با ایدی {user_id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({"message": 'user not found'})

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='read')
    @RequireMethod(allowed_method='POST')
    def warehouse_profile_detail(self, request, *args, **kwargs):
        context = {}
        user_id = fetch_data_from_http_post(request, 'user_id', context)
        try:
            profile = WarehouseProfile.objects.filter(profile__user__id=user_id)
            serializer = WarehouseProfileSerializer(profile, many=True)
            json_response_body = {
                "method": "post",
                "request": f"اطلاعات پروفایل انبارداری کاربر با ایدی {user_id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({"message": 'user not found'})

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='read')
    @RequireMethod(allowed_method='POST')
    def delivery_profile_detail(self, request, *args, **kwargs):
        context = {}
        user_id = fetch_data_from_http_post(request, 'user_id', context)
        try:
            profile = DeliveryProfile.objects.filter(profile__user__id=user_id)
            serializer = DeliveryProfileSerializer(profile, many=True)
            json_response_body = {
                "method": "post",
                "request": f"اطلاعات پروفایل ارسال کاربر با ایدی {user_id}",
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

        return redirect('accounts:profile-list')

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def modify_profile(self, request, *args, **kwargs):
        context = {}
        user_id = fetch_data_from_http_post(request, 'user_id', context)
        try:
            profile = Profile.objects.get(user__id=user_id)

            first_name = fetch_data_from_http_post(request, 'muf_form_user_data_first_name', context)
            last_name = fetch_data_from_http_post(request, 'muf_form_user_data_last_name', context)
            national_code = fetch_data_from_http_post(request, 'muf_form_user_data_national_code', context)
            email = fetch_data_from_http_post(request, 'muf_form_user_data_email', context)
            mobile_phone_number = fetch_data_from_http_post(request, 'muf_form_user_data_mobile_phone_number', context)
            landline = fetch_data_from_http_post(request, 'muf_form_user_data_landline', context)
            card_number = fetch_data_from_http_post(request, 'muf_form_user_data_card_number', context)
            isbn = fetch_data_from_http_post(request, 'muf_form_user_data_isbn', context)
            address = fetch_data_from_http_post(request, 'muf_form_user_data_address', context)
            role_id = fetch_data_from_http_post(request, 'muf_form_user_data_role_id', context)
            password1 = fetch_data_from_http_post(request, 'muf_form_user_data_password1', context)
            password2 = fetch_data_from_http_post(request, 'muf_form_user_data_password2', context)

            if password1 and password2:
                if password1 != password2:
                    return JsonResponse({'message': 'رمز عبور و تکرار رمز عبور یکسان نیستند'})
            elif password1 and not password2:
                return JsonResponse({'message': 'تکرار رمز عبور بدرستی وارد نشده است'})
            elif not password1 and password2:
                return JsonResponse({'message': 'رمز عبور بدرستی وارد نشده است'})
            else:
                pass

            try:
                user = profile.user
                if email:
                    user.email = email
                if password1:
                    user.set_password(password1)
                user.save()
                if first_name:
                    profile.first_name = first_name
                else:
                    first_name = profile.first_name
                    if not profile.first_name:
                        first_name = ''
                if last_name:
                    profile.last_name = last_name
                else:
                    last_name = profile.last_name
                    if not profile.last_name:
                        last_name = ''
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
                    role = Role.objects.get(id=role_id)
                    profile.role_id = role
                    role_title = role.title
                else:
                    role = profile.role
                    if not role:
                        role_title = ''
                    else:
                        role_title = role.title
                profile.save()
                return JsonResponse({'message': f'کاربر با نام کاربری {user.username} ویرایش گردید',
                                     'first_name': first_name, 'last_name': last_name, 'role_title': role_title})
            except Exception as e:
                print(e)
                return JsonResponse({'message': f'کاربر با ایدی {user_id} پیدا نشد'})
        except:
            return JsonResponse({'message': f'کاربر با ایدی {user_id} پیدا نشد'})

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def modify_seller_profile(self, request, *args, **kwargs):
        context = {}
        user_id = fetch_data_from_http_post(request, 'user_id', context)
        try:
            seller_profile = SellerProfile.objects.get(profile__user__id=user_id)
            sale_allowance = fetch_data_from_http_post(request, 'fps_form_profile_seller_sale_allowance', context)
            is_sales_admin = fetch_data_from_http_post(request, 'fps_form_profile_seller_is_sales_admin', context)
            daily_allowed_product_processing_number = fetch_data_from_http_post(request, 'fps_form_profile_seller_daily_allowed_product_processing_number', context)

            if sale_allowance == 'true':
                seller_profile.sale_allowance = True
            else:
                seller_profile.sale_allowance = False

            if is_sales_admin == 'true':
                seller_profile.is_sales_admin = True
            else:
                seller_profile.is_sales_admin = False

            if daily_allowed_product_processing_number:
                seller_profile.daily_allowed_product_processing_number = int(daily_allowed_product_processing_number)

            seller_profile.save()

            seller_profiles = SellerProfile.objects.filter(id=seller_profile.id)
            serializer = SellerProfileSerializer(seller_profiles, many=True)
            json_response_body = {
                "method": "post",
                "message": f'پروفایل فروشندگی کاربر با نام کاربری {seller_profile.profile.user.username} ویرایش گردید',
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({'message': f'کاربر با ایدی {user_id} پیدا نشد'})

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def modify_warehouse_profile(self, request, *args, **kwargs):
        context = {}
        user_id = fetch_data_from_http_post(request, 'user_id', context)
        try:
            warehouse_profile = WarehouseProfile.objects.get(profile__user__id=user_id)
            warehouse_allowance = fetch_data_from_http_post(request, 'fpw_form_profile_warehouse_warehouse_allowance', context)
            is_warehouse_admin = fetch_data_from_http_post(request, 'fpw_form_profile_warehouse_is_warehouse_admin', context)

            if warehouse_allowance == 'true':
                warehouse_profile.warehouse_allowance = True
            else:
                warehouse_profile.warehouse_allowance = False

            if is_warehouse_admin == 'true':
                warehouse_profile.is_warehouse_admin = True
            else:
                warehouse_profile.is_warehouse_admin = False

            warehouse_profile.save()

            warehouse_profiles = WarehouseProfile.objects.filter(id=warehouse_profile.id)
            serializer = WarehouseProfileSerializer(warehouse_profiles, many=True)
            json_response_body = {
                "method": "post",
                "message": f'پروفایل انبارداری کاربر با نام کاربری {warehouse_profile.profile.user.username} ویرایش گردید',
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({'message': f'کاربر با ایدی {user_id} پیدا نشد'})

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def modify_delivery_profile(self, request, *args, **kwargs):
        context = {}
        user_id = fetch_data_from_http_post(request, 'user_id', context)
        try:
            delivery_profile = DeliveryProfile.objects.get(profile__user__id=user_id)
            delivery_allowance = fetch_data_from_http_post(request, 'fpd_form_profile_delivery_delivery_allowance', context)
            is_delivery_admin = fetch_data_from_http_post(request, 'fpd_form_profile_delivery_is_delivery_admin', context)

            if delivery_allowance == 'true':
                delivery_profile.delivery_allowance = True
            else:
                delivery_profile.delivery_allowance = False

            if is_delivery_admin == 'true':
                delivery_profile.is_delivery_admin = True
            else:
                delivery_profile.is_delivery_admin = False

            delivery_profile.save()

            delivery_profiles = DeliveryProfile.objects.filter(id=delivery_profile.id)
            serializer = DeliveryProfileSerializer(delivery_profiles, many=True)
            json_response_body = {
                "method": "post",
                "message": f'پروفایل ارسال کاربر با نام کاربری {delivery_profile.profile.user.username} ویرایش گردید',
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({'message': f'کاربر با ایدی {user_id} پیدا نشد'})

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='delete')
    def delete(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'حذف کاربر {user.username}', 'get_params': request.GET.urlencode()}
            user.delete()
            return redirect(reverse('accounts:profile-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')