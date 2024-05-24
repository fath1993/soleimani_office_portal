from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import Role, Permission
from accounts.templatetags.account_custom_tag import has_access_to_section
from automation.models import RequestedProductProcessing, create_requested_product_processing_report, \
    RequestedProductProcessingReport
from gallery.models import FileGallery
from panel.custom_decorator import CheckLogin, CheckPermissions, RequireMethod
from panel.serializer import RequestedProductProcessingReportSerializer
from portal.models import Product, TeaserMaker
from utilities.http_metod import fetch_data_from_http_post, fetch_files_from_http_post_data, fetch_data_from_http_get


class CreditCardView:
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


class CustomerView:
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


class RequestedProductView:
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


class RequestedProductProcessingView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست درخواست ها', 'get_params': request.GET.urlencode()}

        profile = request.user.user_profile

        q = Q()
        if not request.user.is_superuser:
            try:
                q |= (
                    Q(**{'seller': profile.profile_seller_profile})
                )
            except:
                pass
            try:
                q |= (
                    Q(**{'warehouse_keeper': profile.profile_warehouse_profile})
                )
            except:
                pass
            try:
                q |= (
                    Q(**{'delivery_man': profile.profile_delivery_profile})
                )
            except:
                pass

        requested_product_processing = RequestedProductProcessing.objects.filter(q)
        context['requested_product_processing'] = requested_product_processing

        items_per_page = 50
        paginator = Paginator(requested_product_processing, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/cartable/cartable-list.html', context)

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
    @RequireMethod(allowed_method='POST')
    def reports(self, request, *args, **kwargs):
        context = {}
        requested_product_processing_id = fetch_data_from_http_post(request, 'requested_product_processing_id',
                                                                    context)
        profile = request.user.user_profile

        q = Q()
        q &= (
            Q(**{'pk': requested_product_processing_id})
        )
        if not request.user.is_superuser:
            try:
                q |= (
                    Q(**{'seller': profile.profile_seller_profile})
                )
            except:
                pass
            try:
                q |= (
                    Q(**{'warehouse_keeper': profile.profile_warehouse_profile})
                )
            except:
                pass
            try:
                q |= (
                    Q(**{'delivery_man': profile.profile_delivery_profile})
                )
            except:
                pass
        try:
            requested_product_processing = RequestedProductProcessing.objects.get(q)
            requested_product_processing_reports = RequestedProductProcessingReport.objects.filter(requested_product_processing=requested_product_processing)
            serializer = RequestedProductProcessingReportSerializer(requested_product_processing_reports, many=True)
            json_response_body = {
                "method": "post",
                "request": f"لیست پیام های پردازش محصول درخواستی با ایدی {requested_product_processing.id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({"message": 'requested product processing not found'})



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
    @RequireMethod(allowed_method='POST')
    def change_sale_state(self, request, *args, **kwargs):
        context = {}
        if not request.user.is_superuser:
            try:
                seller_profile = request.user.user_profile.profile_seller_profile
            except:
                return JsonResponse({"message": 'seller profile not found'})
        else:
            seller_profile = None

        requested_product_processing_id = fetch_data_from_http_post(request, 'requested_product_processing_id',
                                                                    context)
        try:
            requested_product_processing = RequestedProductProcessing.objects.get(id=requested_product_processing_id)
            if not request.user.is_superuser:
                if not requested_product_processing.seller == seller_profile:
                    return JsonResponse({"message": 'not authorized seller'})
            mss_status = fetch_data_from_http_post(request, 'mss_status', context)
            mss_message = fetch_data_from_http_post(request, 'mss_message', context)

            create_requested_product_processing_report(requested_product_processing, 'sale', mss_status, mss_message)
            if mss_status == 'sold':
                requested_product_processing.sales_status = 'pending_sales_approval'
                requested_product_processing.save()
                return JsonResponse({"message": 'sold'})
            else:
                requested_product_processing.sales_status = 'canceled'
                requested_product_processing.save()
                requested_product = requested_product_processing.requested_product
                requested_product.is_processed = True
                requested_product.save()
                return JsonResponse({"message": 'canceled'})
        except Exception as e:
            print(e)
            return JsonResponse({"message": 'requested product processing not found'})

    @CheckLogin()
    @RequireMethod(allowed_method='POST')
    def confirm_sale(self, request, *args, **kwargs):
        context = {}
        if not request.user.is_superuser:
            try:
                seller_profile = request.user.user_profile.profile_seller_profile

                if not seller_profile.is_sales_admin:
                    return JsonResponse({"message": 'seller profile is not sale admin'})
            except:
                return JsonResponse({"message": 'seller profile not found'})
        else:
            seller_profile = None

        requested_product_processing_id = fetch_data_from_http_post(request, 'requested_product_processing_id',
                                                                    context)
        try:
            requested_product_processing = RequestedProductProcessing.objects.get(id=requested_product_processing_id)

            msa_status = fetch_data_from_http_post(request, 'ssm_status', context)
            msa_message = fetch_data_from_http_post(request, 'ssm_message', context)

            create_requested_product_processing_report(requested_product_processing, 'sale', msa_status, msa_message)
            if msa_status == 'confirmed':
                requested_product_processing.sales_status = 'sold'
                requested_product_processing.is_confirmed_by_sales_department = True
                requested_product_processing.product_price = requested_product_processing.requested_product
                requested_product_processing.product_number = 1
                requested_product_processing.request_total_income = 1

                requested_product_processing.warehouse_keeper = 1
                requested_product_processing.warehouse_status = 'processing'
                requested_product_processing.save()
                return JsonResponse({"message": 'sold'})
            elif msa_status == 'recheck':
                requested_product_processing.sales_status = 'canceled'
                requested_product_processing.save()
                return JsonResponse({"message": 'canceled'})
            else:
                requested_product_processing.sales_status = 'canceled'
                requested_product_processing.save()
                return JsonResponse({"message": 'canceled'})
        except Exception as e:
            print(e)
            return JsonResponse({"message": 'requested product processing not found'})

    @CheckLogin()
    @RequireMethod(allowed_method='POST')
    def change_warehouse_state(self, request, *args, **kwargs):
        context = {}
        try:
            seller_profile = request.user.user_profile.profile_seller_profile
        except:
            return JsonResponse({"message": 'seller profile not found'})

        requested_product_processing_id = fetch_data_from_http_post(request, 'requested_product_processing_id',
                                                                    context)

        try:
            requested_product_processing = RequestedProductProcessing.objects.get(id=requested_product_processing_id)
            ssm_status = fetch_data_from_http_post(request, 'ssm_status', context)
            ssm_message = fetch_data_from_http_post(request, 'ssm_message', context)
        except:
            return JsonResponse({"message": 'not authorized seller'})

    @CheckLogin()
    @RequireMethod(allowed_method='POST')
    def change_delivery_state(self, request, *args, **kwargs):
        context = {}
        try:
            seller_profile = request.user.user_profile.profile_seller_profile
        except:
            return JsonResponse({"message": 'seller profile not found'})

        requested_product_processing_id = fetch_data_from_http_post(request, 'requested_product_processing_id',
                                                                    context)

        try:
            requested_product_processing = RequestedProductProcessing.objects.get(id=requested_product_processing_id)
            ssm_status = fetch_data_from_http_post(request, 'ssm_status', context)
            ssm_message = fetch_data_from_http_post(request, 'ssm_message', context)
        except:
            return JsonResponse({"message": 'not authorized seller'})