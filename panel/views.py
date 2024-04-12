import random
import time
from functools import wraps

import jdatetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Profile, Role, Permission
from portal.models import Product
from utilities.http_metod import fetch_data_from_http_post, fetch_data_from_http_get
from panel.templatetags.panel_custom_tag import user_section_is_allowed, permission_section_is_allowed, \
    role_section_is_allowed, registrar_is_allowed, communication_channel_is_allowed, forward_to_portal_is_allowed, \
    advertise_content_is_allowed, receiver_is_allowed, reseller_network_is_allowed, teaser_maker_is_allowed, \
    product_is_allowed, resource_section_is_allowed


class CheckLogin:
    def __call__(class_self, view_func):  # we name self to class_self in favor of not being conflict with warp's self
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            return view_func(self, request, *args, **kwargs)
        return wrapper


class CheckPermissions:
    def __init__(class_self, section, allowed_actions=None):
        class_self.section = section
        class_self.allowed_actions = allowed_actions


    def __call__(class_self, view_func):  # we name self to class_self in favor of not being conflict with warp's self
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if class_self.section == 'user':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not user_section_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'permission':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not permission_section_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'role':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not role_section_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'resource':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not resource_section_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'product':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not product_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'teaser_maker':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not teaser_maker_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'reseller_network':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not reseller_network_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'receiver':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not receiver_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'advertise_content':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not advertise_content_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'forward_to_portal':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not forward_to_portal_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'communication_channel':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not communication_channel_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')

            if class_self.section == 'registrar':
                allowed_actions = str(class_self.allowed_actions)
                if (allowed_actions.find('read') != -1 or allowed_actions.find('create') != -1 or
                        allowed_actions.find('modify') != -1 or allowed_actions.find('delete') != -1):
                    if not registrar_is_allowed(request.user, class_self.allowed_actions):
                        return render(request, 'panel/err/err-not-authorized.html')
            return view_func(self, request, *args, **kwargs)
        return wrapper


class DashboardView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    def main(self, request, *args, **kwargs):
        context = {'page_title': 'پنل کاربری - داشبورد'}
        return render(request, 'panel/dashboard.html', context)


class UserView:
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

        return render(request, 'panel/users/user-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='user', allowed_actions='read')
    def detail(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'اطلاعات کاربر *{user.username}*',
                       'user': user, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/users/user-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

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

        return render(request, 'panel/users/user-list.html', context)

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
            return render(request, 'panel/users/user-list.html', context)
        if not password1:
            context['err'] = 'رمز عبور بدرستی وارد نشده است'
            return render(request, 'panel/users/user-list.html', context)
        if not password2:
            context['err'] = 'تکرار رمز عبور بدرستی وارد نشده است'
            return render(request, 'panel/users/user-list.html', context)
        if password1 != password2:
            context['err'] = 'رمز عبور و تکرار رمز عبور یکسان نیستند'
            return render(request, 'panel/users/user-list.html', context)

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
                return render(request, 'panel/users/user-edit.html', context)
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
                        return render(request, 'panel/users/user-list.html', context)
                elif password1 and not password2:
                    context['err'] = 'تکرار رمز عبور بدرستی وارد نشده است'
                    return render(request, 'panel/users/user-list.html', context)
                elif not password1 and password2:
                    context['err'] = 'رمز عبور بدرستی وارد نشده است'
                    return render(request, 'panel/users/user-list.html', context)
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


class PermissionView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='permission', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست مجوز ها', 'get_params': request.GET.urlencode()}
        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست مجوز ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                Q(**{'title__icontains': search})
            )

        permissions = Permission.objects.filter(q).order_by('id')
        context['permissions'] = permissions

        items_per_page = 50
        paginator = Paginator(permissions, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/permissions/permission-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='permission', allowed_actions='read')
    def detail(self, request, permission_id, *args, **kwargs):
        try:
            permission = Permission.objects.get(id=permission_id)
            context = {'page_title': f'اطلاعات مجوز *{permission.title}*',
                       'permission': permission, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/permissions/permission-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='permission', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست مجوز ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'title__icontains': search})
            )
        permissions = Permission.objects.filter(q).order_by('id')
        context['permissions'] = permissions

        items_per_page = 50
        paginator = Paginator(permissions, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/permissions/permission-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='permission', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت مجوز جدید', 'get_params': request.GET.urlencode()}

        title = fetch_data_from_http_post(request, 'first_name', context)
        has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
        read = fetch_data_from_http_post(request, 'national_code', context)
        create = fetch_data_from_http_post(request, 'email', context)
        modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
        delete = fetch_data_from_http_post(request, 'landline', context)

        if not title:
            context['err'] = 'عنوان بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if not has_access_to_section:
            context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if read == 'true':
            read = True
        else:
            read = False
        if create == 'true':
            create = True
        else:
            create = False
        if modify == 'true':
            modify = True
        else:
            modify = False
        if delete == 'true':
            delete = True
        else:
            delete = False

        try:
            User.objects.get(title=title)
            context['err'] = 'مجوز از قبل موجود است'
        except:
            Permission.objects.create(
                title=title,
                has_access_to_section=has_access_to_section,
                read=read,
                create=create,
                modify=modify,
                delete=delete,
            )
            context['message'] = f'مجوز با عنوان {title} ایجاد گردید'

        return redirect('panel:permission-list')

    @CheckLogin()
    @CheckPermissions(section='permission', allowed_actions='modify')
    def modify(self, request, permission_id, *args, **kwargs):
        try:
            permission = Permission.objects.get(id=permission_id)
            context = {'page_title': f'ویرایش اطلاعات مجوز *{permission.title}*',
                       'permission': permission, 'get_params': request.GET.urlencode()}
            if request.method == 'GET':
                return render(request, 'panel/permissions/permission-edit.html', context)
            else:
                title = fetch_data_from_http_post(request, 'first_name', context)
                has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
                read = fetch_data_from_http_post(request, 'national_code', context)
                create = fetch_data_from_http_post(request, 'email', context)
                modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
                delete = fetch_data_from_http_post(request, 'landline', context)

                if not title:
                    context['err'] = 'عنوان بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if not has_access_to_section:
                    context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if read == 'true':
                    read = True
                else:
                    read = False
                if create == 'true':
                    create = True
                else:
                    create = False
                if modify == 'true':
                    modify = True
                else:
                    modify = False
                if delete == 'true':
                    delete = True
                else:
                    delete = False

                if title:
                    permission.title = title
                if has_access_to_section:
                    permission.has_access_to_section = has_access_to_section

                if read:
                    permission.read = read
                if create:
                    permission.create = create
                if modify:
                    permission.modify = modify
                if delete:
                    permission.delete = delete

                permission.save()
                context['message'] = f'مجوز با عنوان {title} ویرایش گردید'
                return redirect(
                    reverse('panel:permission-modify-with-id',
                            kwargs={'permission_id': permission_id}) + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


    @CheckLogin()
    @CheckPermissions(section='permission', allowed_actions='delete')
    def delete(self, request, permission_id, *args, **kwargs):
        try:
            permission = Permission.objects.get(id=permission_id)
            context = {'page_title': f'حذف مجوز {permission.title}', 'get_params': request.GET.urlencode()}
            permission.delete()
            return redirect(reverse('panel:permission-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


class RoleView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='role', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست نقش ها', 'get_params': request.GET.urlencode()}
        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست نقش ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                Q(**{'title__icontains': search})
            )

        roles = Role.objects.filter(q).order_by('id')
        context['roles'] = roles

        items_per_page = 50
        paginator = Paginator(roles, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/roles/role-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='role', allowed_actions='read')
    def detail(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'اطلاعات نقش *{role.title}*',
                       'role': role, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/roles/role-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='role', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست نقش ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'title__icontains': search})
            )
        roles = Role.objects.filter(q).order_by('id')
        context['roles'] = roles

        items_per_page = 50
        paginator = Paginator(roles, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/roles/role-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='role', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت نقش جدید', 'get_params': request.GET.urlencode()}

        title = fetch_data_from_http_post(request, 'first_name', context)
        has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
        read = fetch_data_from_http_post(request, 'national_code', context)
        create = fetch_data_from_http_post(request, 'email', context)
        modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
        delete = fetch_data_from_http_post(request, 'landline', context)

        if not title:
            context['err'] = 'عنوان بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if not has_access_to_section:
            context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if read == 'true':
            read = True
        else:
            read = False
        if create == 'true':
            create = True
        else:
            create = False
        if modify == 'true':
            modify = True
        else:
            modify = False
        if delete == 'true':
            delete = True
        else:
            delete = False

        try:
            User.objects.get(title=title)
            context['err'] = 'مجوز از قبل موجود است'
        except:
            Permission.objects.create(
                title=title,
                has_access_to_section=has_access_to_section,
                read=read,
                create=create,
                modify=modify,
                delete=delete,
            )
            context['message'] = f'مجوز با عنوان {title} ایجاد گردید'

        return redirect('panel:role-list')

    @CheckLogin()
    @CheckPermissions(section='role', allowed_actions='modify')
    def modify(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'ویرایش اطلاعات نقش *{role.title}*',
                       'permission': role, 'get_params': request.GET.urlencode()}
            if request.method == 'GET':
                return render(request, 'panel/roles/role-edit.html', context)
            else:
                title = fetch_data_from_http_post(request, 'first_name', context)
                has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
                read = fetch_data_from_http_post(request, 'national_code', context)
                create = fetch_data_from_http_post(request, 'email', context)
                modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
                delete = fetch_data_from_http_post(request, 'landline', context)

                if not title:
                    context['err'] = 'عنوان بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if not has_access_to_section:
                    context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if read == 'true':
                    read = True
                else:
                    read = False
                if create == 'true':
                    create = True
                else:
                    create = False
                if modify == 'true':
                    modify = True
                else:
                    modify = False
                if delete == 'true':
                    delete = True
                else:
                    delete = False

                if title:
                    role.title = title
                if has_access_to_section:
                    role.has_access_to_section = has_access_to_section

                if read:
                    role.read = read
                if create:
                    role.create = create
                if modify:
                    role.modify = modify
                if delete:
                    role.delete = delete

                role.save()
                context['message'] = f'مجوز با عنوان {title} ویرایش گردید'
                return redirect(
                    reverse('panel:role-modify-with-id',
                            kwargs={'role_id': role_id}) + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


    @CheckLogin()
    @CheckPermissions(section='role', allowed_actions='delete')
    def delete(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'حذف نقش {role.title}', 'get_params': request.GET.urlencode()}
            role.delete()
            return redirect(reverse('panel:role-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


class ProductView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='product', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست محصولات', 'get_params': request.GET.urlencode()}

        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست محصولات شامل *{search}*', 'get_params': request.GET.urlencode()}

            q = Q()
            if search:
                q &= (
                        Q(**{'name': search})
                )

        products = Product.objects.filter().order_by('id')
        context['products'] = products

        items_per_page = 50
        paginator = Paginator(products, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/products/product-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='product', allowed_actions='read')
    def detail(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
            context = {'page_title': f'اطلاعات محصول *{product.name}*',
                       'product': product, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/products/product-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='product', allowed_actions='read')
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

        return render(request, 'panel/users/user-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='product', allowed_actions='create')
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
            return render(request, 'panel/users/user-list.html', context)
        if not password1:
            context['err'] = 'رمز عبور بدرستی وارد نشده است'
            return render(request, 'panel/users/user-list.html', context)
        if not password2:
            context['err'] = 'تکرار رمز عبور بدرستی وارد نشده است'
            return render(request, 'panel/users/user-list.html', context)
        if password1 != password2:
            context['err'] = 'رمز عبور و تکرار رمز عبور یکسان نیستند'
            return render(request, 'panel/users/user-list.html', context)

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
    @CheckPermissions(section='product', allowed_actions='modify')
    def modify(self, request, product_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'ویرایش اطلاعات کاربر *{user.username}*',
                       'user': user, 'get_params': request.GET.urlencode()}

            if request.method == 'GET':
                return render(request, 'panel/users/user-edit.html', context)
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
                        return render(request, 'panel/users/user-list.html', context)
                elif password1 and not password2:
                    context['err'] = 'تکرار رمز عبور بدرستی وارد نشده است'
                    return render(request, 'panel/users/user-list.html', context)
                elif not password1 and password2:
                    context['err'] = 'رمز عبور بدرستی وارد نشده است'
                    return render(request, 'panel/users/user-list.html', context)
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
    @CheckPermissions(section='product', allowed_actions='delete')
    def delete(self, request, product_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'حذف کاربر {user.username}', 'get_params': request.GET.urlencode()}
            user.delete()
            return redirect(reverse('panel:user-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='product', allowed_actions='modify')
    def change_state(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
            context = {'page_title': f'تغییر وضعیت محصول {product.name}', 'get_params': request.GET.urlencode()}
            if product.disabled:
                product.disabled = False
            else:
                product.disabled = True
            product.save()
            return JsonResponse({"product_state": product.disabled})
        except:
            return render(request, 'panel/err/err-not-found.html')

class TeaserMakerView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست مجوز ها', 'get_params': request.GET.urlencode()}
        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست مجوز ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                Q(**{'title__icontains': search})
            )

        permissions = Permission.objects.filter(q).order_by('id')
        context['permissions'] = permissions

        items_per_page = 50
        paginator = Paginator(permissions, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/permissions/permission-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='read')
    def detail(self, request, permission_id, *args, **kwargs):
        try:
            permission = Permission.objects.get(id=permission_id)
            context = {'page_title': f'اطلاعات مجوز *{permission.title}*',
                       'permission': permission, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/permissions/permission-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست مجوز ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'title__icontains': search})
            )
        permissions = Permission.objects.filter(q).order_by('id')
        context['permissions'] = permissions

        items_per_page = 50
        paginator = Paginator(permissions, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/permissions/permission-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت مجوز جدید', 'get_params': request.GET.urlencode()}

        title = fetch_data_from_http_post(request, 'first_name', context)
        has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
        read = fetch_data_from_http_post(request, 'national_code', context)
        create = fetch_data_from_http_post(request, 'email', context)
        modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
        delete = fetch_data_from_http_post(request, 'landline', context)

        if not title:
            context['err'] = 'عنوان بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if not has_access_to_section:
            context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if read == 'true':
            read = True
        else:
            read = False
        if create == 'true':
            create = True
        else:
            create = False
        if modify == 'true':
            modify = True
        else:
            modify = False
        if delete == 'true':
            delete = True
        else:
            delete = False

        try:
            User.objects.get(title=title)
            context['err'] = 'مجوز از قبل موجود است'
        except:
            Permission.objects.create(
                title=title,
                has_access_to_section=has_access_to_section,
                read=read,
                create=create,
                modify=modify,
                delete=delete,
            )
            context['message'] = f'مجوز با عنوان {title} ایجاد گردید'

        return redirect('panel:permission-list')

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='modify')
    def modify(self, request, permission_id, *args, **kwargs):
        try:
            permission = Permission.objects.get(id=permission_id)
            context = {'page_title': f'ویرایش اطلاعات مجوز *{permission.title}*',
                       'permission': permission, 'get_params': request.GET.urlencode()}
            if request.method == 'GET':
                return render(request, 'panel/permissions/permission-edit.html', context)
            else:
                title = fetch_data_from_http_post(request, 'first_name', context)
                has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
                read = fetch_data_from_http_post(request, 'national_code', context)
                create = fetch_data_from_http_post(request, 'email', context)
                modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
                delete = fetch_data_from_http_post(request, 'landline', context)

                if not title:
                    context['err'] = 'عنوان بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if not has_access_to_section:
                    context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if read == 'true':
                    read = True
                else:
                    read = False
                if create == 'true':
                    create = True
                else:
                    create = False
                if modify == 'true':
                    modify = True
                else:
                    modify = False
                if delete == 'true':
                    delete = True
                else:
                    delete = False

                if title:
                    permission.title = title
                if has_access_to_section:
                    permission.has_access_to_section = has_access_to_section

                if read:
                    permission.read = read
                if create:
                    permission.create = create
                if modify:
                    permission.modify = modify
                if delete:
                    permission.delete = delete

                permission.save()
                context['message'] = f'مجوز با عنوان {title} ویرایش گردید'
                return redirect(
                    reverse('panel:permission-modify-with-id',
                            kwargs={'permission_id': permission_id}) + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='delete')
    def delete(self, request, permission_id, *args, **kwargs):
        try:
            permission = Permission.objects.get(id=permission_id)
            context = {'page_title': f'حذف مجوز {permission.title}', 'get_params': request.GET.urlencode()}
            permission.delete()
            return redirect(reverse('panel:permission-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


class ResellerNetworkView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='reseller_network', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست نقش ها', 'get_params': request.GET.urlencode()}
        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست نقش ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                Q(**{'title__icontains': search})
            )

        roles = Role.objects.filter(q).order_by('id')
        context['roles'] = roles

        items_per_page = 50
        paginator = Paginator(roles, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/roles/role-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='reseller_network', allowed_actions='read')
    def detail(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'اطلاعات نقش *{role.title}*',
                       'role': role, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/roles/role-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='reseller_network', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست نقش ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'title__icontains': search})
            )
        roles = Role.objects.filter(q).order_by('id')
        context['roles'] = roles

        items_per_page = 50
        paginator = Paginator(roles, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/roles/role-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='reseller_network', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت نقش جدید', 'get_params': request.GET.urlencode()}

        title = fetch_data_from_http_post(request, 'first_name', context)
        has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
        read = fetch_data_from_http_post(request, 'national_code', context)
        create = fetch_data_from_http_post(request, 'email', context)
        modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
        delete = fetch_data_from_http_post(request, 'landline', context)

        if not title:
            context['err'] = 'عنوان بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if not has_access_to_section:
            context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if read == 'true':
            read = True
        else:
            read = False
        if create == 'true':
            create = True
        else:
            create = False
        if modify == 'true':
            modify = True
        else:
            modify = False
        if delete == 'true':
            delete = True
        else:
            delete = False

        try:
            User.objects.get(title=title)
            context['err'] = 'مجوز از قبل موجود است'
        except:
            Permission.objects.create(
                title=title,
                has_access_to_section=has_access_to_section,
                read=read,
                create=create,
                modify=modify,
                delete=delete,
            )
            context['message'] = f'مجوز با عنوان {title} ایجاد گردید'

        return redirect('panel:role-list')

    @CheckLogin()
    @CheckPermissions(section='reseller_network', allowed_actions='modify')
    def modify(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'ویرایش اطلاعات نقش *{role.title}*',
                       'permission': role, 'get_params': request.GET.urlencode()}
            if request.method == 'GET':
                return render(request, 'panel/roles/role-edit.html', context)
            else:
                title = fetch_data_from_http_post(request, 'first_name', context)
                has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
                read = fetch_data_from_http_post(request, 'national_code', context)
                create = fetch_data_from_http_post(request, 'email', context)
                modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
                delete = fetch_data_from_http_post(request, 'landline', context)

                if not title:
                    context['err'] = 'عنوان بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if not has_access_to_section:
                    context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if read == 'true':
                    read = True
                else:
                    read = False
                if create == 'true':
                    create = True
                else:
                    create = False
                if modify == 'true':
                    modify = True
                else:
                    modify = False
                if delete == 'true':
                    delete = True
                else:
                    delete = False

                if title:
                    role.title = title
                if has_access_to_section:
                    role.has_access_to_section = has_access_to_section

                if read:
                    role.read = read
                if create:
                    role.create = create
                if modify:
                    role.modify = modify
                if delete:
                    role.delete = delete

                role.save()
                context['message'] = f'مجوز با عنوان {title} ویرایش گردید'
                return redirect(
                    reverse('panel:role-modify-with-id',
                            kwargs={'role_id': role_id}) + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


    @CheckLogin()
    @CheckPermissions(section='reseller_network', allowed_actions='delete')
    def delete(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'حذف نقش {role.title}', 'get_params': request.GET.urlencode()}
            role.delete()
            return redirect(reverse('panel:role-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


class ReceiverView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='receiver', allowed_actions='read')
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

        return render(request, 'panel/users/user-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='receiver', allowed_actions='read')
    def detail(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'اطلاعات کاربر *{user.username}*',
                       'user': user, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/users/user-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='receiver', allowed_actions='read')
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

        return render(request, 'panel/users/user-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='receiver', allowed_actions='create')
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
            return render(request, 'panel/users/user-list.html', context)
        if not password1:
            context['err'] = 'رمز عبور بدرستی وارد نشده است'
            return render(request, 'panel/users/user-list.html', context)
        if not password2:
            context['err'] = 'تکرار رمز عبور بدرستی وارد نشده است'
            return render(request, 'panel/users/user-list.html', context)
        if password1 != password2:
            context['err'] = 'رمز عبور و تکرار رمز عبور یکسان نیستند'
            return render(request, 'panel/users/user-list.html', context)

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
    @CheckPermissions(section='receiver', allowed_actions='modify')
    def modify(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'ویرایش اطلاعات کاربر *{user.username}*',
                       'user': user, 'get_params': request.GET.urlencode()}

            if request.method == 'GET':
                return render(request, 'panel/users/user-edit.html', context)
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
                        return render(request, 'panel/users/user-list.html', context)
                elif password1 and not password2:
                    context['err'] = 'تکرار رمز عبور بدرستی وارد نشده است'
                    return render(request, 'panel/users/user-list.html', context)
                elif not password1 and password2:
                    context['err'] = 'رمز عبور بدرستی وارد نشده است'
                    return render(request, 'panel/users/user-list.html', context)
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
    @CheckPermissions(section='receiver', allowed_actions='delete')
    def delete(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'حذف کاربر {user.username}', 'get_params': request.GET.urlencode()}
            user.delete()
            return redirect(reverse('panel:user-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


class AdvertiseContentView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست مجوز ها', 'get_params': request.GET.urlencode()}
        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست مجوز ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                Q(**{'title__icontains': search})
            )

        permissions = Permission.objects.filter(q).order_by('id')
        context['permissions'] = permissions

        items_per_page = 50
        paginator = Paginator(permissions, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/permissions/permission-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='read')
    def detail(self, request, permission_id, *args, **kwargs):
        try:
            permission = Permission.objects.get(id=permission_id)
            context = {'page_title': f'اطلاعات مجوز *{permission.title}*',
                       'permission': permission, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/permissions/permission-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست مجوز ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'title__icontains': search})
            )
        permissions = Permission.objects.filter(q).order_by('id')
        context['permissions'] = permissions

        items_per_page = 50
        paginator = Paginator(permissions, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/permissions/permission-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت مجوز جدید', 'get_params': request.GET.urlencode()}

        title = fetch_data_from_http_post(request, 'first_name', context)
        has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
        read = fetch_data_from_http_post(request, 'national_code', context)
        create = fetch_data_from_http_post(request, 'email', context)
        modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
        delete = fetch_data_from_http_post(request, 'landline', context)

        if not title:
            context['err'] = 'عنوان بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if not has_access_to_section:
            context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if read == 'true':
            read = True
        else:
            read = False
        if create == 'true':
            create = True
        else:
            create = False
        if modify == 'true':
            modify = True
        else:
            modify = False
        if delete == 'true':
            delete = True
        else:
            delete = False

        try:
            User.objects.get(title=title)
            context['err'] = 'مجوز از قبل موجود است'
        except:
            Permission.objects.create(
                title=title,
                has_access_to_section=has_access_to_section,
                read=read,
                create=create,
                modify=modify,
                delete=delete,
            )
            context['message'] = f'مجوز با عنوان {title} ایجاد گردید'

        return redirect('panel:permission-list')

    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='modify')
    def modify(self, request, permission_id, *args, **kwargs):
        try:
            permission = Permission.objects.get(id=permission_id)
            context = {'page_title': f'ویرایش اطلاعات مجوز *{permission.title}*',
                       'permission': permission, 'get_params': request.GET.urlencode()}
            if request.method == 'GET':
                return render(request, 'panel/permissions/permission-edit.html', context)
            else:
                title = fetch_data_from_http_post(request, 'first_name', context)
                has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
                read = fetch_data_from_http_post(request, 'national_code', context)
                create = fetch_data_from_http_post(request, 'email', context)
                modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
                delete = fetch_data_from_http_post(request, 'landline', context)

                if not title:
                    context['err'] = 'عنوان بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if not has_access_to_section:
                    context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if read == 'true':
                    read = True
                else:
                    read = False
                if create == 'true':
                    create = True
                else:
                    create = False
                if modify == 'true':
                    modify = True
                else:
                    modify = False
                if delete == 'true':
                    delete = True
                else:
                    delete = False

                if title:
                    permission.title = title
                if has_access_to_section:
                    permission.has_access_to_section = has_access_to_section

                if read:
                    permission.read = read
                if create:
                    permission.create = create
                if modify:
                    permission.modify = modify
                if delete:
                    permission.delete = delete

                permission.save()
                context['message'] = f'مجوز با عنوان {title} ویرایش گردید'
                return redirect(
                    reverse('panel:permission-modify-with-id',
                            kwargs={'permission_id': permission_id}) + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='delete')
    def delete(self, request, permission_id, *args, **kwargs):
        try:
            permission = Permission.objects.get(id=permission_id)
            context = {'page_title': f'حذف مجوز {permission.title}', 'get_params': request.GET.urlencode()}
            permission.delete()
            return redirect(reverse('panel:permission-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


class ForwardToPortalView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='forward_to_portal', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست نقش ها', 'get_params': request.GET.urlencode()}
        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست نقش ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                Q(**{'title__icontains': search})
            )

        roles = Role.objects.filter(q).order_by('id')
        context['roles'] = roles

        items_per_page = 50
        paginator = Paginator(roles, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/roles/role-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='forward_to_portal', allowed_actions='read')
    def detail(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'اطلاعات نقش *{role.title}*',
                       'role': role, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/roles/role-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='forward_to_portal', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست نقش ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'title__icontains': search})
            )
        roles = Role.objects.filter(q).order_by('id')
        context['roles'] = roles

        items_per_page = 50
        paginator = Paginator(roles, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/roles/role-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='forward_to_portal', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت نقش جدید', 'get_params': request.GET.urlencode()}

        title = fetch_data_from_http_post(request, 'first_name', context)
        has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
        read = fetch_data_from_http_post(request, 'national_code', context)
        create = fetch_data_from_http_post(request, 'email', context)
        modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
        delete = fetch_data_from_http_post(request, 'landline', context)

        if not title:
            context['err'] = 'عنوان بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if not has_access_to_section:
            context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if read == 'true':
            read = True
        else:
            read = False
        if create == 'true':
            create = True
        else:
            create = False
        if modify == 'true':
            modify = True
        else:
            modify = False
        if delete == 'true':
            delete = True
        else:
            delete = False

        try:
            User.objects.get(title=title)
            context['err'] = 'مجوز از قبل موجود است'
        except:
            Permission.objects.create(
                title=title,
                has_access_to_section=has_access_to_section,
                read=read,
                create=create,
                modify=modify,
                delete=delete,
            )
            context['message'] = f'مجوز با عنوان {title} ایجاد گردید'

        return redirect('panel:role-list')

    @CheckLogin()
    @CheckPermissions(section='forward_to_portal', allowed_actions='modify')
    def modify(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'ویرایش اطلاعات نقش *{role.title}*',
                       'permission': role, 'get_params': request.GET.urlencode()}
            if request.method == 'GET':
                return render(request, 'panel/roles/role-edit.html', context)
            else:
                title = fetch_data_from_http_post(request, 'first_name', context)
                has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
                read = fetch_data_from_http_post(request, 'national_code', context)
                create = fetch_data_from_http_post(request, 'email', context)
                modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
                delete = fetch_data_from_http_post(request, 'landline', context)

                if not title:
                    context['err'] = 'عنوان بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if not has_access_to_section:
                    context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if read == 'true':
                    read = True
                else:
                    read = False
                if create == 'true':
                    create = True
                else:
                    create = False
                if modify == 'true':
                    modify = True
                else:
                    modify = False
                if delete == 'true':
                    delete = True
                else:
                    delete = False

                if title:
                    role.title = title
                if has_access_to_section:
                    role.has_access_to_section = has_access_to_section

                if read:
                    role.read = read
                if create:
                    role.create = create
                if modify:
                    role.modify = modify
                if delete:
                    role.delete = delete

                role.save()
                context['message'] = f'مجوز با عنوان {title} ویرایش گردید'
                return redirect(
                    reverse('panel:role-modify-with-id',
                            kwargs={'role_id': role_id}) + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


    @CheckLogin()
    @CheckPermissions(section='role', allowed_actions='delete')
    def delete(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'حذف نقش {role.title}', 'get_params': request.GET.urlencode()}
            role.delete()
            return redirect(reverse('panel:role-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


class CommunicationChannelView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='communication_channel', allowed_actions='read')
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

        return render(request, 'panel/users/user-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='communication_channel', allowed_actions='read')
    def detail(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'اطلاعات کاربر *{user.username}*',
                       'user': user, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/users/user-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='communication_channel', allowed_actions='read')
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

        return render(request, 'panel/users/user-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='communication_channel', allowed_actions='create')
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
            return render(request, 'panel/users/user-list.html', context)
        if not password1:
            context['err'] = 'رمز عبور بدرستی وارد نشده است'
            return render(request, 'panel/users/user-list.html', context)
        if not password2:
            context['err'] = 'تکرار رمز عبور بدرستی وارد نشده است'
            return render(request, 'panel/users/user-list.html', context)
        if password1 != password2:
            context['err'] = 'رمز عبور و تکرار رمز عبور یکسان نیستند'
            return render(request, 'panel/users/user-list.html', context)

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
    @CheckPermissions(section='communication_channel', allowed_actions='modify')
    def modify(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'ویرایش اطلاعات کاربر *{user.username}*',
                       'user': user, 'get_params': request.GET.urlencode()}

            if request.method == 'GET':
                return render(request, 'panel/users/user-edit.html', context)
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
                        return render(request, 'panel/users/user-list.html', context)
                elif password1 and not password2:
                    context['err'] = 'تکرار رمز عبور بدرستی وارد نشده است'
                    return render(request, 'panel/users/user-list.html', context)
                elif not password1 and password2:
                    context['err'] = 'رمز عبور بدرستی وارد نشده است'
                    return render(request, 'panel/users/user-list.html', context)
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
    @CheckPermissions(section='communication_channel', allowed_actions='delete')
    def delete(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            context = {'page_title': f'حذف کاربر {user.username}', 'get_params': request.GET.urlencode()}
            user.delete()
            return redirect(reverse('panel:user-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


class RegistrarView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست مجوز ها', 'get_params': request.GET.urlencode()}
        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست مجوز ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                Q(**{'title__icontains': search})
            )

        permissions = Permission.objects.filter(q).order_by('id')
        context['permissions'] = permissions

        items_per_page = 50
        paginator = Paginator(permissions, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/permissions/permission-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='read')
    def detail(self, request, permission_id, *args, **kwargs):
        try:
            permission = Permission.objects.get(id=permission_id)
            context = {'page_title': f'اطلاعات مجوز *{permission.title}*',
                       'permission': permission, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/permissions/permission-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست مجوز ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'title__icontains': search})
            )
        permissions = Permission.objects.filter(q).order_by('id')
        context['permissions'] = permissions

        items_per_page = 50
        paginator = Paginator(permissions, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/permissions/permission-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت مجوز جدید', 'get_params': request.GET.urlencode()}

        title = fetch_data_from_http_post(request, 'first_name', context)
        has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
        read = fetch_data_from_http_post(request, 'national_code', context)
        create = fetch_data_from_http_post(request, 'email', context)
        modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
        delete = fetch_data_from_http_post(request, 'landline', context)

        if not title:
            context['err'] = 'عنوان بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if not has_access_to_section:
            context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
            return render(request, 'panel/permissions/permission-list.html', context)
        if read == 'true':
            read = True
        else:
            read = False
        if create == 'true':
            create = True
        else:
            create = False
        if modify == 'true':
            modify = True
        else:
            modify = False
        if delete == 'true':
            delete = True
        else:
            delete = False

        try:
            User.objects.get(title=title)
            context['err'] = 'مجوز از قبل موجود است'
        except:
            Permission.objects.create(
                title=title,
                has_access_to_section=has_access_to_section,
                read=read,
                create=create,
                modify=modify,
                delete=delete,
            )
            context['message'] = f'مجوز با عنوان {title} ایجاد گردید'

        return redirect('panel:permission-list')

    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='modify')
    def modify(self, request, permission_id, *args, **kwargs):
        try:
            permission = Permission.objects.get(id=permission_id)
            context = {'page_title': f'ویرایش اطلاعات مجوز *{permission.title}*',
                       'permission': permission, 'get_params': request.GET.urlencode()}
            if request.method == 'GET':
                return render(request, 'panel/permissions/permission-edit.html', context)
            else:
                title = fetch_data_from_http_post(request, 'first_name', context)
                has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
                read = fetch_data_from_http_post(request, 'national_code', context)
                create = fetch_data_from_http_post(request, 'email', context)
                modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
                delete = fetch_data_from_http_post(request, 'landline', context)

                if not title:
                    context['err'] = 'عنوان بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if not has_access_to_section:
                    context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if read == 'true':
                    read = True
                else:
                    read = False
                if create == 'true':
                    create = True
                else:
                    create = False
                if modify == 'true':
                    modify = True
                else:
                    modify = False
                if delete == 'true':
                    delete = True
                else:
                    delete = False

                if title:
                    permission.title = title
                if has_access_to_section:
                    permission.has_access_to_section = has_access_to_section

                if read:
                    permission.read = read
                if create:
                    permission.create = create
                if modify:
                    permission.modify = modify
                if delete:
                    permission.delete = delete

                permission.save()
                context['message'] = f'مجوز با عنوان {title} ویرایش گردید'
                return redirect(
                    reverse('panel:permission-modify-with-id',
                            kwargs={'permission_id': permission_id}) + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='delete')
    def delete(self, request, permission_id, *args, **kwargs):
        try:
            permission = Permission.objects.get(id=permission_id)
            context = {'page_title': f'حذف مجوز {permission.title}', 'get_params': request.GET.urlencode()}
            permission.delete()
            return redirect(reverse('panel:permission-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

