from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import Role, Permission
from gallery.models import FileGallery
from panel.custom_decorator import CheckLogin, CheckPermissions, RequireMethod
from portal.models import Product, TeaserMaker
from utilities.http_metod import fetch_data_from_http_post, fetch_files_from_http_post_data, fetch_data_from_http_get


class DashboardView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    def main(self, request, *args, **kwargs):
        context = {'page_title': 'پنل کاربری - داشبورد'}
        return render(request, 'panel/dashboard.html', context)

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
        context = {}
        search = fetch_data_from_http_get(request, 'search', context)
        product_type = fetch_data_from_http_get(request, 'type', context)
        is_active = fetch_data_from_http_get(request, 'is_active', context)
        color = fetch_data_from_http_get(request, 'color', context)
        weight_from = fetch_data_from_http_get(request, 'weight_from', context)
        weight_to = fetch_data_from_http_get(request, 'weight_to', context)
        size_from = fetch_data_from_http_get(request, 'size_from', context)
        size_to = fetch_data_from_http_get(request, 'size_to', context)
        product_price_from = fetch_data_from_http_get(request, 'product_price_from', context)
        product_price_to = fetch_data_from_http_get(request, 'product_price_to', context)
        shipping_price_from = fetch_data_from_http_get(request, 'shipping_price_from', context)
        shipping_price_to = fetch_data_from_http_get(request, 'shipping_price_to', context)
        send_link_price_from = fetch_data_from_http_get(request, 'send_link_price_from', context)
        send_link_price_to = fetch_data_from_http_get(request, 'send_link_price_to', context)
        packing_price_from = fetch_data_from_http_get(request, 'packing_price_from', context)
        packing_price_to = fetch_data_from_http_get(request, 'packing_price_to', context)
        seller_commission_from = fetch_data_from_http_get(request, 'seller_commission_from', context)
        seller_commission_to = fetch_data_from_http_get(request, 'seller_commission_to', context)

        page_title = f''''''
        q = Q()
        if search:
            page_title += f'search: {search}, '
            if search.isdigit():
                q &= (
                    Q(**{'id__exact': search})
                )
            else:
                q &= (
                        Q(**{'name__icontains': search}) |
                        Q(**{'code': search})
                )

        if product_type:
            page_title += f'product_type: {product_type}, '
            q &= (
                Q(**{'type': product_type})
            )

        if is_active:
            page_title += f'is_active: {is_active}, '
            if is_active == 'فعال':
                is_active = True
            else:
                is_active = False
            q &= (
                Q(**{'is_active': is_active})
            )

        if color:
            page_title += f'color: {color}, '
            q &= (
                Q(**{'color': color})
            )

        if weight_from:
            page_title += f'weight_from: {weight_from}, '
            q &= (
                Q(**{'weight__gte': int(weight_from)})
            )

        if weight_to:
            page_title += f'weight_to: {weight_to}, '
            q &= (
                Q(**{'weight__lte': int(weight_to)})
            )

        if size_from:
            page_title += f'size_from: {size_from}, '
            q &= (
                Q(**{'size__gte': float(size_from)})
            )

        if size_to:
            page_title += f'size_to: {size_to}, '
            q &= (
                Q(**{'size__lte': float(size_to)})
            )

        if product_price_from:
            page_title += f'product_price_from: {product_price_from}, '
            q &= (
                Q(**{'product_price__gte': int(product_price_from)})
            )

        if product_price_to:
            page_title += f'product_price_to: {product_price_to}, '
            q &= (
                Q(**{'product_price__lte': int(product_price_to)})
            )

        if shipping_price_from:
            page_title += f'shipping_price_from: {shipping_price_from}, '
            q &= (
                Q(**{'shipping_price__gte': int(shipping_price_from)})
            )

        if shipping_price_to:
            page_title += f'shipping_price_to: {shipping_price_to}, '
            q &= (
                Q(**{'shipping_price__lte': int(shipping_price_to)})
            )

        if send_link_price_from:
            page_title += f'send_link_price_from: {send_link_price_from}, '
            q &= (
                Q(**{'send_link_price__gte': int(send_link_price_from)})
            )

        if send_link_price_to:
            page_title += f'send_link_price_to: {send_link_price_to}, '
            q &= (
                Q(**{'send_link_price__lte': int(send_link_price_to)})
            )

        if packing_price_from:
            page_title += f'packing_price_from: {packing_price_from}, '
            q &= (
                Q(**{'packing_price__gte': int(packing_price_from)})
            )

        if packing_price_to:
            page_title += f'packing_price_to: {packing_price_to}, '
            q &= (
                Q(**{'packing_price__lte': int(packing_price_to)})
            )

        if seller_commission_from:
            page_title += f'seller_commission_from: {seller_commission_from}, '
            q &= (
                Q(**{'seller_commission__gte': int(seller_commission_from)})
            )

        if seller_commission_to:
            page_title += f'seller_commission_to: {seller_commission_to}, '
            q &= (
                Q(**{'seller_commission__lte': int(seller_commission_to)})
            )
        context['page_title'] = f'لیست محصولات شامل *{page_title}*'
        context['get_params'] = request.GET.urlencode()

        products = Product.objects.filter(q).order_by('id')
        context['products'] = products

        items_per_page = 50
        paginator = Paginator(products, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/products/product-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='product', allowed_actions='create')
    @RequireMethod(allowed_method='POST')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت محصول جدید', 'get_params': request.GET.urlencode()}

        name = fetch_data_from_http_post(request, 'name', context)
        product_type = fetch_data_from_http_post(request, 'type', context)
        code = fetch_data_from_http_post(request, 'code', context)
        weight = fetch_data_from_http_post(request, 'weight', context)
        size = fetch_data_from_http_post(request, 'size', context)
        color = fetch_data_from_http_post(request, 'color', context)
        images = fetch_files_from_http_post_data(request, 'images', context)
        videos = fetch_files_from_http_post_data(request, 'videos', context)
        product_price = fetch_data_from_http_post(request, 'product_price', context)
        shipping_price = fetch_data_from_http_post(request, 'shipping_price', context)
        send_link_price = fetch_data_from_http_post(request, 'send_link_price', context)
        packing_price = fetch_data_from_http_post(request, 'packing_price', context)
        seller_commission = fetch_data_from_http_post(request, 'seller_commission', context)
        is_active = fetch_data_from_http_post(request, 'is_active', context)

        if not name:
            context['err'] = 'نام محصول بدرستی وارد نشده است'
            return render(request, 'panel/products/product-list.html', context)
        if not product_type:
            context['err'] = 'نوع محصول بدرستی وارد نشده است'
            return render(request, 'panel/products/product-list.html', context)
        if not code:
            context['err'] = 'کد محصول بدرستی وارد نشده است'
            return render(request, 'panel/products/product-list.html', context)
        if not weight:
            context['err'] = 'وزن محصول بدرستی وارد نشده است'
            return render(request, 'panel/products/product-list.html', context)
        if not size:
            context['err'] = 'سایز محصول بدرستی وارد نشده است'
            return render(request, 'panel/products/product-list.html', context)
        if not color:
            context['err'] = 'رنگ محصول بدرستی وارد نشده است'
            return render(request, 'panel/products/product-list.html', context)
        if not product_price:
            context['err'] = 'هزینه خام محصول بدرستی وارد نشده است'
            return render(request, 'panel/products/product-list.html', context)
        if not shipping_price:
            context['err'] = 'هزینه حمل محصول بدرستی وارد نشده است'
            return render(request, 'panel/products/product-list.html', context)
        if not send_link_price:
            context['err'] = 'هزینه ارسال لینک محصول بدرستی وارد نشده است'
            return render(request, 'panel/products/product-list.html', context)
        if not packing_price:
            context['err'] = 'هزینه بسته بندی محصول بدرستی وارد نشده است'
            return render(request, 'panel/products/product-list.html', context)
        if not seller_commission:
            context['err'] = 'نام محصول بدرستی وارد نشده است'
            return render(request, 'panel/products/product-list.html', context)
        if is_active == 'true':
            is_active = True
        else:
            is_active = False

        try:
            Product.objects.get(code=code)
            context['err'] = f'محصول با کد {code} از قبل موجود است'
            return render(request, 'panel/products/product-list.html', context)
        except:
            new_product = Product.objects.create(
                name=name,
                type=product_type,
                code=code,
                weight=weight,
                size=size,
                color=color,
                product_price=product_price,
                shipping_price=shipping_price,
                send_link_price=send_link_price,
                packing_price=packing_price,
                seller_commission=seller_commission,
                is_active=is_active,
                created_by=request.user,
                updated_by=request.user,
            )

            for image in images:
                try:
                    new_file = FileGallery.objects.create(
                        alt=image.name,
                        file=image,
                        created_by=request.user,
                    )
                    new_product.images.add(new_file)
                except:
                    pass

            for video in videos:
                try:
                    new_file = FileGallery.objects.create(
                        alt=video.name,
                        file=video,
                        created_by=request.user,
                    )
                    new_product.videos.add(new_file)
                except:
                    pass

            context['message'] = f'محصول با کد {code} ایجاد گردید'
            return redirect('panel:product-list')

    @CheckLogin()
    @CheckPermissions(section='product', allowed_actions='modify')
    def modify(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
            context = {'page_title': f'ویرایش اطلاعات محصول *{product.name}*',
                       'product': product, 'get_params': request.GET.urlencode()}

            if request.method == 'GET':
                return render(request, 'panel/products/product-edit.html', context)
            else:
                name = fetch_data_from_http_post(request, 'name', context)
                product_type = fetch_data_from_http_post(request, 'type', context)
                code = fetch_data_from_http_post(request, 'code', context)
                weight = fetch_data_from_http_post(request, 'weight', context)
                size = fetch_data_from_http_post(request, 'size', context)
                color = fetch_data_from_http_post(request, 'color', context)
                images = fetch_files_from_http_post_data(request, 'images', context)
                videos = fetch_files_from_http_post_data(request, 'videos', context)
                product_price = fetch_data_from_http_post(request, 'product_price', context)
                shipping_price = fetch_data_from_http_post(request, 'shipping_price', context)
                send_link_price = fetch_data_from_http_post(request, 'send_link_price', context)
                packing_price = fetch_data_from_http_post(request, 'packing_price', context)
                seller_commission = fetch_data_from_http_post(request, 'seller_commission', context)
                is_active = fetch_data_from_http_post(request, 'is_active', context)

                try:
                    if name:
                        product.name = name
                    if product_type:
                        product.product_type = product_type
                    if code:
                        product.code = code
                    if weight:
                        product.weight = weight
                    if size:
                        product.size = size
                    if color:
                        product.color = color
                    if product_price:
                        product.product_price = product_price
                    if shipping_price:
                        product.shipping_price = shipping_price
                    if send_link_price:
                        product.send_link_price = send_link_price
                    if packing_price:
                        product.packing_price = packing_price
                    if seller_commission:
                        product.seller_commission = seller_commission
                    if is_active == 'true':
                        is_active = True
                    else:
                        is_active = False
                    product.is_active = is_active
                    product.save()
                    if images:
                        for image in images:
                            try:
                                new_file = FileGallery.objects.create(
                                    alt=image.name,
                                    file=image,
                                    created_by=request.user,
                                )
                                product.images.add(new_file)
                            except:
                                pass
                    if videos:
                        for video in videos:
                            try:
                                new_file = FileGallery.objects.create(
                                    alt=video.name,
                                    file=video,
                                    created_by=request.user,
                                )
                                product.videos.add(new_file)
                            except:
                                pass
                    context['message'] = f'محصول با شناسه یکتا {product.id} ویرایش گردید'
                    return redirect(
                        reverse('panel:product-detail-with-id',
                                kwargs={'product_id': product_id}) + f'?{request.GET.urlencode()}')
                except:
                    return render(request, 'panel/err/err-not-found.html')
        except Exception as e:
            print(e)
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='product', allowed_actions='delete')
    @RequireMethod(allowed_method='POST')
    def delete_file(self, request, file_id, *args, **kwargs):
        try:
            file = FileGallery.objects.get(id=file_id)
            file.delete()
            return JsonResponse({"message": 'deleted'})
        except:
            return JsonResponse({"message": 'failed'})

    @CheckLogin()
    @CheckPermissions(section='product', allowed_actions='delete')
    def delete(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
            context = {'page_title': f'حذف محصول {product.name}', 'get_params': request.GET.urlencode()}

            images = product.images.all()
            videos = product.videos.all()

            for image in images:
                image.delete()
            for video in videos:
                video.delete()

            product.delete()
            return redirect(reverse('panel:product-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='product', allowed_actions='modify')
    def change_state(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
            context = {'page_title': f'تغییر وضعیت محصول {product.name}', 'get_params': request.GET.urlencode()}
            if product.is_active:
                product.is_active = False
                product_is_active = 'false'
            else:
                product.is_active = True
                product_is_active = 'true'
            product.save()
            return JsonResponse({"product_is_active": product_is_active})
        except:
            return render(request, 'panel/err/err-not-found.html')


class TeaserMakerView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست تیزر ساز ها', 'get_params': request.GET.urlencode()}

        teaser_makers = TeaserMaker.objects.filter().order_by('id')
        context['teaser_makers'] = teaser_makers

        items_per_page = 50
        paginator = Paginator(teaser_makers, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/teaser-maker/teaser-maker-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='read')
    def detail(self, request, teaser_maker_id, *args, **kwargs):
        try:
            teaser_maker = TeaserMaker.objects.get(id=teaser_maker_id)
            context = {'page_title': f'اطلاعات تیزر ساز *{teaser_maker.name}*',
                       'teaser_maker': teaser_maker, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/teaser-maker/teaser-maker-detail.html', context)
        except Exception as e:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        context = {}
        search = fetch_data_from_http_get(request, 'search', context)
        content_type = fetch_data_from_http_get(request, 'content_type', context)
        is_active = fetch_data_from_http_get(request, 'is_active', context)
        address = fetch_data_from_http_get(request, 'address', context)
        phone_number = fetch_data_from_http_get(request, 'phone_number', context)
        creation_price_from = fetch_data_from_http_get(request, 'creation_price_from', context)
        creation_price_to = fetch_data_from_http_get(request, 'creation_price_to', context)
        editing_price_from = fetch_data_from_http_get(request, 'editing_price_from', context)
        editing_price_to = fetch_data_from_http_get(request, 'editing_price_to', context)

        page_title = f''''''
        q = Q()
        if search:
            page_title += f'search: {search}, '
            if search.isdigit():
                q &= (
                    Q(**{'id': search})
                )
            else:
                q &= (
                        Q(**{'name__icontains': search}) |
                        Q(**{'code': search})
                )

        if content_type:
            page_title += f'content_type: {content_type}, '
            q &= (
                Q(**{'content_type': content_type})
            )

        if is_active:
            page_title += f'is_active: {is_active}, '
            if is_active == 'فعال':
                is_active = True
            else:
                is_active = False
            q &= (
                Q(**{'is_active': is_active})
            )

        if address:
            page_title += f'address: {address}, '
            q &= (
                Q(**{'address__icontains': address})
            )

        if phone_number:
            page_title += f'phone_number: {phone_number}, '
            q &= (
                Q(**{'phone_number__icontains': phone_number})
            )

        if creation_price_from:
            page_title += f'creation_price_from: {creation_price_from}, '
            q &= (
                Q(**{'creation_price__gte': int(creation_price_from)})
            )

        if creation_price_to:
            page_title += f'creation_price_to: {creation_price_to}, '
            q &= (
                Q(**{'creation_price__lte': int(creation_price_to)})
            )

        if editing_price_from:
            page_title += f'editing_price_from: {editing_price_from}, '
            q &= (
                Q(**{'editing_price__gte': int(editing_price_from)})
            )

        if editing_price_to:
            page_title += f'editing_price_to: {editing_price_to}, '
            q &= (
                Q(**{'editing_price__lte': int(editing_price_to)})
            )

        context['page_title'] = f'لیست تیزر ساز ها شامل *{page_title}*'
        context['get_params'] = request.GET.urlencode()

        teaser_makers = TeaserMaker.objects.filter(q).order_by('id')
        context['teaser_makers'] = teaser_makers

        items_per_page = 50
        paginator = Paginator(teaser_makers, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/teaser-maker/teaser-maker-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='create')
    @RequireMethod(allowed_method='POST')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت تیزر ساز جدید', 'get_params': request.GET.urlencode()}

        name = fetch_data_from_http_post(request, 'name', context)
        content_type = fetch_data_from_http_post(request, 'content_type', context)
        code = fetch_data_from_http_post(request, 'code', context)
        address = fetch_data_from_http_post(request, 'address', context)
        phone_number = fetch_data_from_http_post(request, 'phone_number', context)
        creation_price = fetch_data_from_http_post(request, 'creation_price', context)
        editing_price = fetch_data_from_http_post(request, 'editing_price', context)
        is_active = fetch_data_from_http_post(request, 'is_active', context)

        if not name:
            context['err'] = 'نام تیزر ساز بدرستی وارد نشده است'
            return render(request, 'panel/teaser-maker/teaser-maker-list.html', context)
        if not content_type:
            context['err'] = 'نوع محتوا تیزر ساز بدرستی وارد نشده است'
            return render(request, 'panel/teaser-maker/teaser-maker-list.html', context)
        if not code:
            context['err'] = 'کد تیزر ساز بدرستی وارد نشده است'
            return render(request, 'panel/teaser-maker/teaser-maker-list.html', context)
        if not address:
            context['err'] = 'آدرس تیزر ساز بدرستی وارد نشده است'
            return render(request, 'panel/teaser-maker/teaser-maker-list.html', context)
        if not phone_number:
            context['err'] = 'شماره تماس تیزر ساز بدرستی وارد نشده است'
            return render(request, 'panel/teaser-maker/teaser-maker-list.html', context)
        if not creation_price:
            context['err'] = 'هزینه ساخت تیزر ساز بدرستی وارد نشده است'
            return render(request, 'panel/teaser-maker/teaser-maker-list.html', context)
        if not editing_price:
            context['err'] = 'هزینه ویرایش تیزر ساز محصول بدرستی وارد نشده است'
            return render(request, 'panel/teaser-maker/teaser-maker-list.html', context)
        if is_active == 'true':
            is_active = True
        else:
            is_active = False

        try:
            TeaserMaker.objects.get(code=code)
            context['err'] = f'تیزر ساز با کد {code} از قبل موجود است'
            return render(request, 'panel/teaser-maker/teaser-maker-list.html', context)
        except:
            new_teaser_maker = TeaserMaker.objects.create(
                name=name,
                content_type=content_type,
                code=code,
                address=address,
                phone_number=phone_number,
                creation_price=creation_price,
                editing_price=editing_price,
                created_by=request.user,
                updated_by=request.user,
                is_active=is_active,
            )

            context['message'] = f'تیزر ساز با کد {code} ایجاد گردید'
            return redirect('panel:teaser-maker-list')

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='modify')
    def modify(self, request, teaser_maker_id, *args, **kwargs):
        try:
            teaser_maker = TeaserMaker.objects.get(id=teaser_maker_id)
            context = {'page_title': f'ویرایش اطلاعات تیزر ساز *{teaser_maker.name}*',
                       'teaser_maker': teaser_maker, 'get_params': request.GET.urlencode()}

            if request.method == 'GET':
                return render(request, 'panel/teaser-maker/teaser-maker-edit.html', context)
            else:
                name = fetch_data_from_http_post(request, 'name', context)
                content_type = fetch_data_from_http_post(request, 'content_type', context)
                code = fetch_data_from_http_post(request, 'code', context)
                address = fetch_data_from_http_post(request, 'address', context)
                phone_number = fetch_data_from_http_post(request, 'phone_number', context)
                creation_price = fetch_data_from_http_post(request, 'creation_price', context)
                editing_price = fetch_data_from_http_post(request, 'editing_price', context)
                is_active = fetch_data_from_http_post(request, 'is_active', context)

                try:
                    if name:
                        teaser_maker.name = name
                    if content_type:
                        teaser_maker.content_type = content_type
                    if code:
                        teaser_maker.code = code
                    if address:
                        teaser_maker.address = address
                    if phone_number:
                        teaser_maker.phone_number = phone_number
                    if creation_price:
                        teaser_maker.creation_price = creation_price
                    if editing_price:
                        teaser_maker.editing_price = editing_price
                    if is_active == 'true':
                        is_active = True
                    else:
                        is_active = False
                    teaser_maker.is_active = is_active
                    teaser_maker.save()
                    context['message'] = f'تیزر ساز با شناسه یکتا {teaser_maker.id} ویرایش گردید'
                    return redirect(
                        reverse('panel:teaser-maker-detail-with-id',
                                kwargs={'teaser_maker_id': teaser_maker_id}) + f'?{request.GET.urlencode()}')
                except:
                    return render(request, 'panel/err/err-not-found.html')
        except Exception as e:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='delete')
    def delete(self, request, teaser_maker_id, *args, **kwargs):
        try:
            teaser_maker = TeaserMaker.objects.get(id=teaser_maker_id)
            context = {'page_title': f'حذف تیزر ساز {teaser_maker.name}', 'get_params': request.GET.urlencode()}
            teaser_maker.delete()
            return redirect(reverse('panel:teaser-maker-list') + f'?{request.GET.urlencode()}')
        except Exception as e:
            print(e)
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='modify')
    def change_state(self, request, teaser_maker_id, *args, **kwargs):
        try:
            teaser_maker = TeaserMaker.objects.get(id=teaser_maker_id)
            context = {'page_title': f'تغییر وضعیت تیزر ساز {teaser_maker.name}', 'get_params': request.GET.urlencode()}
            if teaser_maker.is_active:
                teaser_maker.is_active = False
                teaser_maker_is_active = 'false'
            else:
                teaser_maker.is_active = True
                teaser_maker_is_active = 'true'
            teaser_maker.save()
            return JsonResponse({"teaser_maker_is_active": teaser_maker_is_active})
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
