from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from gallery.models import FileGallery, create_file
from accounts.custom_decorator import CheckLogin, CheckPermissions, RequireMethod
from resource.models import Product, TeaserMaker, ResellerNetwork, Receiver, AdvertiseContent, ForwardToPortal, \
    CommunicationChannel, Registrar
from resource.serializer import RegistrarSerializer, ReceiverSerializer, ResellerNetworkSerializer
from utilities.http_metod import fetch_data_from_http_post, fetch_files_from_http_post_data, fetch_data_from_http_get


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

        return render(request, 'panel/portal/products/product-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='product', allowed_actions='read')
    def detail(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
            context = {'page_title': f'اطلاعات محصول *{product.name}*',
                       'product': product, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/portal/products/product-detail.html', context)
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

        return render(request, 'panel/portal/products/product-list.html', context)

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
            return render(request, 'panel/portal/products/product-list.html', context)
        if not product_type:
            context['err'] = 'نوع محصول بدرستی وارد نشده است'
            return render(request, 'panel/portal/products/product-list.html', context)
        if not code:
            context['err'] = 'کد محصول بدرستی وارد نشده است'
            return render(request, 'panel/portal/products/product-list.html', context)
        if not weight:
            context['err'] = 'وزن محصول بدرستی وارد نشده است'
            return render(request, 'panel/portal/products/product-list.html', context)
        if not size:
            context['err'] = 'سایز محصول بدرستی وارد نشده است'
            return render(request, 'panel/portal/products/product-list.html', context)
        if not color:
            context['err'] = 'رنگ محصول بدرستی وارد نشده است'
            return render(request, 'panel/portal/products/product-list.html', context)
        if not product_price:
            context['err'] = 'هزینه خام محصول بدرستی وارد نشده است'
            return render(request, 'panel/portal/products/product-list.html', context)
        if not shipping_price:
            context['err'] = 'هزینه حمل محصول بدرستی وارد نشده است'
            return render(request, 'panel/portal/products/product-list.html', context)
        if not send_link_price:
            context['err'] = 'هزینه ارسال لینک محصول بدرستی وارد نشده است'
            return render(request, 'panel/portal/products/product-list.html', context)
        if not packing_price:
            context['err'] = 'هزینه بسته بندی محصول بدرستی وارد نشده است'
            return render(request, 'panel/portal/products/product-list.html', context)
        if not seller_commission:
            context['err'] = 'نام محصول بدرستی وارد نشده است'
            return render(request, 'panel/portal/products/product-list.html', context)
        if is_active == 'true':
            is_active = True
        else:
            is_active = False

        try:
            Product.objects.get(code=code)
            context['err'] = f'محصول با کد {code} از قبل موجود است'
            return render(request, 'panel/portal/products/product-list.html', context)
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
            return redirect('resource:product-list')

    @CheckLogin()
    @CheckPermissions(section='product', allowed_actions='modify')
    def modify(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
            context = {'page_title': f'ویرایش اطلاعات محصول *{product.name}*',
                       'product': product, 'get_params': request.GET.urlencode()}

            if request.method == 'GET':
                return render(request, 'panel/portal/products/product-edit.html', context)
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
                        reverse('resource:product-detail-with-id',
                                kwargs={'product_id': product_id}) + f'?{request.GET.urlencode()}')
                except:
                    return render(request, 'panel/err/err-not-found.html')
        except Exception as e:
            print(e)
            return render(request, 'panel/err/err-not-found.html')

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
            return redirect(reverse('resource:product-list') + f'?{request.GET.urlencode()}')
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

        return render(request, 'panel/portal/teaser-maker/teaser-maker-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='read')
    def detail(self, request, teaser_maker_id, *args, **kwargs):
        try:
            teaser_maker = TeaserMaker.objects.get(id=teaser_maker_id)
            context = {'page_title': f'اطلاعات تیزر ساز *{teaser_maker.name}*',
                       'teaser_maker': teaser_maker, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/portal/teaser-maker/teaser-maker-detail.html', context)
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

        return render(request, 'panel/portal/teaser-maker/teaser-maker-list.html', context)

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
            return render(request, 'panel/portal/teaser-maker/teaser-maker-list.html', context)
        if not content_type:
            context['err'] = 'نوع محتوا تیزر ساز بدرستی وارد نشده است'
            return render(request, 'panel/portal/teaser-maker/teaser-maker-list.html', context)
        if not code:
            context['err'] = 'کد تیزر ساز بدرستی وارد نشده است'
            return render(request, 'panel/portal/teaser-maker/teaser-maker-list.html', context)
        if not address:
            context['err'] = 'آدرس تیزر ساز بدرستی وارد نشده است'
            return render(request, 'panel/portal/teaser-maker/teaser-maker-list.html', context)
        if not phone_number:
            context['err'] = 'شماره تماس تیزر ساز بدرستی وارد نشده است'
            return render(request, 'panel/portal/teaser-maker/teaser-maker-list.html', context)
        if not creation_price:
            context['err'] = 'هزینه ساخت تیزر ساز بدرستی وارد نشده است'
            return render(request, 'panel/portal/teaser-maker/teaser-maker-list.html', context)
        if not editing_price:
            context['err'] = 'هزینه ویرایش تیزر ساز محصول بدرستی وارد نشده است'
            return render(request, 'panel/portal/teaser-maker/teaser-maker-list.html', context)
        if is_active == 'true':
            is_active = True
        else:
            is_active = False

        try:
            TeaserMaker.objects.get(code=code)
            context['err'] = f'تیزر ساز با کد {code} از قبل موجود است'
            return render(request, 'panel/portal/teaser-maker/teaser-maker-list.html', context)
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
            return redirect('resource:teaser-maker-list')

    @CheckLogin()
    @CheckPermissions(section='teaser_maker', allowed_actions='modify')
    def modify(self, request, teaser_maker_id, *args, **kwargs):
        try:
            teaser_maker = TeaserMaker.objects.get(id=teaser_maker_id)
            context = {'page_title': f'ویرایش اطلاعات تیزر ساز *{teaser_maker.name}*',
                       'teaser_maker': teaser_maker, 'get_params': request.GET.urlencode()}

            if request.method == 'GET':
                return render(request, 'panel/portal/teaser-maker/teaser-maker-edit.html', context)
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
        context = {'page_title': 'لیست شبکه های تبلیغ کننده', 'get_params': request.GET.urlencode()}
        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست شبکه های تبلیغ کننده شامل *{search}*',
                       'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'name__icontains': search}) |
                    Q(**{'network_type__icontains': search}) |
                    Q(**{'code__icontains': search}) |
                    Q(**{'broadcast_direction__icontains': search}) |
                    Q(**{'company_name__icontains': search}) |
                    Q(**{'owner_name__icontains': search}) |
                    Q(**{'broker_name__icontains': search})
            )

        reseller_networks = ResellerNetwork.objects.filter(q).order_by('id')
        context['reseller_networks'] = reseller_networks

        items_per_page = 50
        paginator = Paginator(reseller_networks, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='reseller_network', allowed_actions='read')
    @RequireMethod(allowed_method='POST')
    def detail(self, request, *args, **kwargs):
        context = {}
        reseller_network_id = fetch_data_from_http_post(request, 'reseller_network_id', context)
        try:
            reseller_network = ResellerNetwork.objects.filter(id=reseller_network_id)
            serializer = ResellerNetworkSerializer(reseller_network, many=True)
            json_response_body = {
                "method": "post",
                "request": f"دیتای شبکه تبلیغاتی با شناسه یکتای {reseller_network_id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'failed'})

    @CheckLogin()
    @CheckPermissions(section='reseller_network', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست شبکه های تبلیغ کننده شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'name__icontains': search}) |
                    Q(**{'network_type__icontains': search}) |
                    Q(**{'code__icontains': search}) |
                    Q(**{'broadcast_direction__icontains': search}) |
                    Q(**{'company_name__icontains': search}) |
                    Q(**{'owner_name__icontains': search}) |
                    Q(**{'broker_name__icontains': search})
            )
        reseller_networks = ResellerNetwork.objects.filter(q).order_by('id')
        context['reseller_networks'] = reseller_networks

        items_per_page = 50
        paginator = Paginator(reseller_networks, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='reseller_network', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت شبکه تبلیغ کننده جدید', 'get_params': request.GET.urlencode()}

        name = fetch_data_from_http_post(request, 'name', context)
        network_type = fetch_data_from_http_post(request, 'network_type', context)
        code = fetch_data_from_http_post(request, 'code', context)
        broadcast_direction = fetch_data_from_http_post(request, 'broadcast_direction', context)
        company_name = fetch_data_from_http_post(request, 'company_name', context)
        owner_name = fetch_data_from_http_post(request, 'owner_name', context)
        broker_name = fetch_data_from_http_post(request, 'broker_name', context)
        broadcast_price = fetch_data_from_http_post(request, 'broadcast_price', context)
        subtitle_price = fetch_data_from_http_post(request, 'subtitle_price', context)

        if not name:
            context['err'] = 'نام بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)
        if not network_type:
            context['err'] = 'نوع شبکه بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)
        if not code:
            context['err'] = 'کد بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)
        if not broadcast_direction:
            context['err'] = 'جهت شبکه بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)
        if not company_name:
            context['err'] = 'نام کمپانی بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)
        if not owner_name:
            context['err'] = 'نام مالک بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)
        if not broker_name:
            context['err'] = 'نام کارگزار بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)
        if not broadcast_price:
            context['err'] = 'قیمت برادکست بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)
        if not subtitle_price:
            context['err'] = 'قیمت زیرنویس بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)

        try:
            ResellerNetwork.objects.get(code=code)
            context['err'] = 'شبکه تبلیغ کننده از قبل موجود است'
        except:
            ResellerNetwork.objects.create(
                name=name,
                network_type=network_type,
                code=code,
                broadcast_direction=broadcast_direction,
                company_name=company_name,
                owner_name=owner_name,
                broker_name=broker_name,
                broadcast_price=broadcast_price,
                subtitle_price=subtitle_price,
                created_by=request.user,
                updated_by=request.user,
                is_active=True,
            )
            context['message'] = f'شبکه تبلیغ کننده با عنوان {name} ایجاد گردید'

        return redirect('resource:reseller-network-list')

    @CheckLogin()
    @CheckPermissions(section='reseller_network', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def modify(self, request, *args, **kwargs):
        context = {}
        reseller_network_id = fetch_data_from_http_post(request, 'reseller_network_id', context)
        try:
            reseller_network = ResellerNetwork.objects.get(id=reseller_network_id)
            context = {'page_title': f'ویرایش شبکه تبلیغ کننده با شناسه یکتای *{reseller_network.code}*',
                       'reseller_network': reseller_network, 'get_params': request.GET.urlencode()}
            name = fetch_data_from_http_post(request, 'fmrn_form_modal_reseller_network_data_name', context, False)
            network_type = fetch_data_from_http_post(request, 'fmrn_form_modal_reseller_network_data_network_type', context, False)
            broadcast_direction = fetch_data_from_http_post(request, 'fmrn_form_modal_reseller_network_data_broadcast_direction', context, False)
            company_name = fetch_data_from_http_post(request, 'fmrn_form_modal_reseller_network_data_company_name', context, False)
            owner_name = fetch_data_from_http_post(request, 'fmrn_form_modal_reseller_network_data_owner_name', context)
            broker_name = fetch_data_from_http_post(request, 'fmrn_form_modal_reseller_network_data_broker_name', context, False)
            broadcast_price = fetch_data_from_http_post(request, 'fmrn_form_modal_reseller_network_data_broadcast_price', context)
            subtitle_price = fetch_data_from_http_post(request, 'fmrn_form_modal_reseller_network_data_subtitle_price', context, False)
            is_active = fetch_data_from_http_post(request, 'fmrn_form_modal_reseller_network_data_is_active', context)

            if name:
                reseller_network.name = name
            if network_type:
                reseller_network.network_type = network_type
            if broadcast_direction:
                reseller_network.broadcast_direction = broadcast_direction
            if company_name:
                reseller_network.company_name = company_name
            if owner_name:
                reseller_network.owner_name = owner_name
            if broker_name:
                reseller_network.broker_name = broker_name
            if broadcast_price:
                reseller_network.broadcast_price = broadcast_price
            if subtitle_price:
                reseller_network.subtitle_price = subtitle_price
            if is_active == 'true':
                reseller_network.is_active = True
            else:
                reseller_network.is_active = False
            reseller_network.save()

            return JsonResponse({'message': f'شبکه تبلیغ کننده با شناسه یکتا {reseller_network.code} ویرایش گردید'})
        except:
            return JsonResponse({'message': f'reseller network not found'})

    @CheckLogin()
    @CheckPermissions(section='reseller_network', allowed_actions='delete')
    def delete(self, request, reseller_network_id, *args, **kwargs):
        try:
            reseller_network = ResellerNetwork.objects.get(id=reseller_network_id)
            context = {'page_title': f'حذف شبکه تبلیغ کننده {reseller_network.code}',
                       'get_params': request.GET.urlencode()}
            reseller_network.delete()
            return redirect(reverse('panel:reseller-network-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='reseller_network', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def change_state(self, request, *args, **kwargs):
        context = {}
        reseller_network_id = fetch_data_from_http_post(request, 'reseller_network_id', context)
        try:
            reseller_network = ResellerNetwork.objects.get(id=reseller_network_id)
            context = {'page_title': f'تغییر وضعیت شبکه های تبلیغ کننده {reseller_network.code}',
                       'get_params': request.GET.urlencode()}
            if reseller_network.is_active:
                reseller_network.is_active = False
                reseller_network_is_active = 'false'
            else:
                reseller_network.is_active = True
                reseller_network_is_active = 'true'
            reseller_network.save()
            return JsonResponse({"reseller_network_is_active": reseller_network_is_active})
        except:
            return render(request, 'panel/err/err-not-found.html')


class ReceiverView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='receiver', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست دریافت کننده ها', 'get_params': request.GET.urlencode()}

        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست دریافت کننده ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'name__icontains': search}) |
                    Q(**{'receiving_type__icontains': search}) |
                    Q(**{'code__icontains': search}) |
                    Q(**{'receiver_phone_number__icontains': search})
            )

        receiver = Receiver.objects.filter(q).order_by('id')
        context['receiver'] = receiver

        items_per_page = 50
        paginator = Paginator(receiver, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/receiver/receiver-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='receiver', allowed_actions='read')
    @RequireMethod(allowed_method='POST')
    def detail(self, request, *args, **kwargs):
        context = {}
        receiver_id = fetch_data_from_http_post(request, 'receiver_id', context)
        try:
            receiver = Receiver.objects.filter(id=receiver_id)
            serializer = ReceiverSerializer(receiver, many=True)
            json_response_body = {
                "method": "post",
                "request": f"دیتای دریافت کننده با ایدی {receiver_id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'failed'})

    @CheckLogin()
    @CheckPermissions(section='receiver', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست دریافت کنندگان شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'name__icontains': search}) |
                    Q(**{'receiving_type__icontains': search}) |
                    Q(**{'code__icontains': search}) |
                    Q(**{'receiver_phone_number__icontains': search})
            )
        receiver = Receiver.objects.filter(q).order_by('id')
        context['receiver'] = receiver

        items_per_page = 50
        paginator = Paginator(receiver, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/receiver/receiver-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='receiver', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت شبکه تبلیغ کننده جدید', 'get_params': request.GET.urlencode()}

        name = fetch_data_from_http_post(request, 'name', context)
        receiving_type = fetch_data_from_http_post(request, 'receiving_type', context)
        code = fetch_data_from_http_post(request, 'code', context)
        receiver_phone_number = fetch_data_from_http_post(request, 'receiver_phone_number', context)
        price = fetch_data_from_http_post(request, 'price', context)

        if not name:
            context['err'] = 'نام بدرستی وارد نشده است'
            return render(request, 'panel/portal/receiver/receiver-list.html', context)
        if not receiving_type:
            context['err'] = 'نوع دریافت کننده بدرستی وارد نشده است'
            return render(request, 'panel/portal/receiver/receiver-list.html', context)
        if not code:
            context['err'] = 'کد بدرستی وارد نشده است'
            return render(request, 'panel/portal/receiver/receiver-list.html', context)
        if not receiver_phone_number:
            context['err'] = 'شماره دریافت کننده بدرستی وارد نشده است'
            return render(request, 'panel/portal/receiver/receiver-list.html', context)
        if not price:
            context['err'] = 'قیمت بدرستی وارد نشده است'
            return render(request, 'panel/portal/receiver/receiver-list.html', context)

        try:
            Receiver.objects.get(code=code)
            context['err'] = f'دریافت کننده با کد {code} از قبل موجود است'
        except:
            Receiver.objects.create(
                name=name,
                receiving_type=receiving_type,
                code=code,
                receiver_phone_number=receiver_phone_number,
                price=price,
                created_by=request.user,
                updated_by=request.user,
                is_active=True,
            )
            context['message'] = f'دریافت کننده با شناسه یکتا {code} ایجاد گردید'

        return redirect('resource:receiver-list')

    @CheckLogin()
    @CheckPermissions(section='receiver', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def modify(self, request, *args, **kwargs):
        context = {}
        receiver_id = fetch_data_from_http_post(request, 'receiver_id', context)
        try:
            receiver = Receiver.objects.get(id=receiver_id)
            context = {'page_title': f'ویرایش دریافت کننده با شناسه یکتای *{receiver.code}*',
                       'receiver': receiver, 'get_params': request.GET.urlencode()}
            name = fetch_data_from_http_post(request, 'fr_form_modal_receiver_data_name', context, False)
            receiving_type = fetch_data_from_http_post(request, 'fr_form_modal_receiver_data_receiving_type', context, False)
            receiver_phone_number = fetch_data_from_http_post(request, 'fr_form_modal_receiver_data_receiver_phone_number', context, False)
            price = fetch_data_from_http_post(request, 'fr_form_modal_receiver_data_price', context, False)
            is_active = fetch_data_from_http_post(request, 'fr_form_modal_receiver_data_is_active', context)

            if name:
                receiver.name = name
            if receiving_type:
                receiver.receiving_type = receiving_type
            if receiver_phone_number:
                receiver.receiver_phone_number = receiver_phone_number
            if price:
                receiver.price = price
            if is_active == 'true':
                receiver.is_active = True
            else:
                receiver.is_active = False
            receiver.save()

            return JsonResponse({'message': f'دریافت کننده با شناسه یکتا {receiver.code} ویرایش گردید'})
        except:
            return JsonResponse({'message': f'receiver not found'})

    @CheckLogin()
    @CheckPermissions(section='receiver', allowed_actions='delete')
    def delete(self, request, receiver_id, *args, **kwargs):
        try:
            receiver = Receiver.objects.get(id=receiver_id)
            context = {'page_title': f'حذف دریافت کننده {receiver.code}', 'get_params': request.GET.urlencode()}
            receiver.delete()
            return redirect(reverse('resource:receiver-delete-with-id') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='receiver', allowed_actions='modify')
    def change_state(self, request, *args, **kwargs):
        context = {}
        receiver_id = fetch_data_from_http_post(request, 'receiver_id', context)
        try:
            receiver = Receiver.objects.get(id=receiver_id)
            context = {'page_title': f'تغییر وضعیت دریافت کننده {receiver.code}',
                       'get_params': request.GET.urlencode()}
            if receiver.is_active:
                receiver.is_active = False
                receiver_is_active = 'false'
            else:
                receiver.is_active = True
                receiver_is_active = 'true'
            receiver.save()
            return JsonResponse({"receiver_is_active": receiver_is_active})
        except:
            return render(request, 'panel/err/err-not-found.html')


class AdvertiseContentView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست محتوای تبلیغاتی', 'get_params': request.GET.urlencode()}

        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست محتوای تبلیغاتی شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'name__icontains': search}) |
                    Q(**{'advertise_content_type__icontains': search}) |
                    Q(**{'code__icontains': search})
            )

        advertise_contents = AdvertiseContent.objects.filter(q).order_by('id')
        context['advertise_contents'] = advertise_contents

        items_per_page = 50
        paginator = Paginator(advertise_contents, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='read')
    def detail(self, request, advertise_content_id, *args, **kwargs):
        try:
            advertise_content = AdvertiseContent.objects.get(id=advertise_content_id)
            context = {'page_title': f'اطلاعات محتوای تبلیغاتی *{advertise_content.code}*',
                       'advertise_content': advertise_content, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/portal/advertise-content/advertise-content-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست محتوای تبلیغاتی شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'name__icontains': search}) |
                    Q(**{'advertise_content_type__icontains': search}) |
                    Q(**{'code__icontains': search})
            )
        advertise_contents = AdvertiseContent.objects.filter(q).order_by('id')
        context['advertise_contents'] = advertise_contents

        items_per_page = 50
        paginator = Paginator(advertise_contents, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت شبکه تبلیغ کننده جدید', 'get_params': request.GET.urlencode()}

        name = fetch_data_from_http_post(request, 'name', context)
        advertise_content_type = fetch_data_from_http_post(request, 'advertise_content_type', context)
        code = fetch_data_from_http_post(request, 'code', context)
        contents = fetch_files_from_http_post_data(request, 'contents', context)
        product_id = fetch_data_from_http_post(request, 'product_id', context)
        receiver_id = fetch_data_from_http_post(request, 'receiver_id', context)
        teaser_maker_id = fetch_data_from_http_post(request, 'teaser_maker_id', context)
        reseller_network_id = fetch_data_from_http_post(request, 'reseller_network_id', context)

        if not name:
            context['err'] = 'نام بدرستی وارد نشده است'
            return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)
        if not advertise_content_type:
            context['err'] = 'نوع محتوای تبلیغاتی بدرستی وارد نشده است'
            return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)
        if not code:
            context['err'] = 'کد بدرستی وارد نشده است'
            return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)
        if not product_id:
            context['err'] = 'محصول بدرستی وارد نشده است'
            return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)
        else:
            try:
                product = Product.objects.get(id=product_id)
            except:
                context['err'] = 'محصول بدرستی وارد نشده است'
                return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)
        if not receiver_id:
            context['err'] = 'دریافت کننده بدرستی وارد نشده است'
            return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)
        else:
            try:
                receiver = Receiver.objects.get(id=receiver_id)
            except:
                context['err'] = 'دریافت کننده بدرستی وارد نشده است'
                return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)
        if not teaser_maker_id:
            context['err'] = 'تیزرساز بدرستی وارد نشده است'
            return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)
        else:
            try:
                teaser_maker = TeaserMaker.objects.get(id=teaser_maker_id)
            except:
                context['err'] = 'تیزرساز بدرستی وارد نشده است'
                return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)
        if not reseller_network_id:
            context['err'] = 'شبکه تبلیغ کننده بدرستی وارد نشده است'
            return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)
        else:
            try:
                reseller_network = ResellerNetwork.objects.get(id=reseller_network_id)
            except:
                context['err'] = 'شبکه تبلیغ کننده بدرستی وارد نشده است'
                return render(request, 'panel/portal/advertise-content/advertise-content-list.html', context)
        try:
            AdvertiseContent.objects.get(code=code)
            context['err'] = f'محتوای تبلیغاتی با کد {code} از قبل موجود است'
        except:
            new_advertise_content = AdvertiseContent.objects.create(
                name=name,
                advertise_content_type=advertise_content_type,
                code=code,
                product=product,
                receiver=receiver,
                teaser_maker=teaser_maker,
                reseller_network=reseller_network,
                created_by=request.user,
                updated_by=request.user,
                is_active=True,
            )

            for content in contents:
                new_file = create_file(request, content)
                new_advertise_content.content.add(new_file)
            context['message'] = f'محتوای تبلیغاتی با شناسه یکتا {code} ایجاد گردید'

        return redirect('panel:advertise-content-list')

    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='modify')
    def modify(self, request, advertise_content_id, *args, **kwargs):
        try:
            advertise_content = AdvertiseContent.objects.get(id=advertise_content_id)
            context = {'page_title': f'ویرایش اطلاعات محتوای تبلیغاتی *{advertise_content.code}*',
                       'advertise_content': advertise_content, 'get_params': request.GET.urlencode()}
            if request.method == 'GET':
                return render(request, 'panel/portal/advertise-content/advertise-content-edit.html', context)
            else:
                name = fetch_data_from_http_post(request, 'name', context, False)
                advertise_content_type = fetch_data_from_http_post(request, 'advertise_content_type', context, False)
                code = fetch_data_from_http_post(request, 'code', context, False)
                contents = fetch_files_from_http_post_data(request, 'contents', context)
                product_id = fetch_data_from_http_post(request, 'product_id', context)
                receiver_id = fetch_data_from_http_post(request, 'receiver_id', context)
                teaser_maker_id = fetch_data_from_http_post(request, 'teaser_maker_id', context)
                reseller_network_id = fetch_data_from_http_post(request, 'reseller_network_id', context)
                is_active = fetch_data_from_http_post(request, 'is_active', context, False)

                if name:
                    advertise_content.name = name
                if advertise_content_type:
                    advertise_content.advertise_content_type = advertise_content_type
                if code:
                    advertise_content.code = code
                if product_id:
                    try:
                        advertise_content.product = Product.objects.get(id=product_id)
                    except:
                        pass
                if receiver_id:
                    try:
                        advertise_content.receiver = Receiver.objects.get(id=receiver_id)
                    except:
                        pass
                if teaser_maker_id:
                    try:
                        advertise_content.teaser_maker = TeaserMaker.objects.get(id=teaser_maker_id)
                    except:
                        pass
                if reseller_network_id:
                    try:
                        advertise_content.reseller_network = ResellerNetwork.objects.get(id=reseller_network_id)
                    except:
                        pass
                if is_active == 'true':
                    advertise_content.is_active = True
                else:
                    advertise_content.is_active = False

                advertise_content.save()

                for content in contents:
                    try:
                        file = FileGallery.objects.create(
                            alt=content.name,
                            file=content,
                            created_by=request.user,
                        )
                        advertise_content.content.add(file)
                    except:
                        pass

                context['message'] = f'محتوای تبلیغاتی با کد {advertise_content.code} ویرایش گردید'
                return redirect(
                    reverse('panel:advertise-content-modify-with-id',
                            kwargs={'advertise_content_id': advertise_content_id}) + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='delete')
    def delete(self, request, advertise_content_id, *args, **kwargs):
        try:
            advertise_content = AdvertiseContent.objects.get(id=advertise_content_id)
            context = {'page_title': f'حذف محتوای تبلیغاتی {advertise_content.code}',
                       'get_params': request.GET.urlencode()}
            advertise_content.delete()
            return redirect(reverse('panel:advertise-content-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='advertise_content', allowed_actions='modify')
    def change_state(self, request, advertise_content_id, *args, **kwargs):
        try:
            advertise_content = AdvertiseContent.objects.get(id=advertise_content_id)
            context = {'page_title': f'تغییر وضعیت محتوای تبلیغاتی {advertise_content.code}',
                       'get_params': request.GET.urlencode()}
            if advertise_content.is_active:
                advertise_content.is_active = False
                advertise_content_is_active = 'false'
            else:
                advertise_content.is_active = True
                advertise_content_is_active = 'true'
            advertise_content.save()
            return JsonResponse({"advertise_content_is_active": advertise_content_is_active})
        except:
            return render(request, 'panel/err/err-not-found.html')


class ForwardToPortalView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='forward_to_portal', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست انتقال دهنده ها', 'get_params': request.GET.urlencode()}

        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست انتقال دهنده ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'name__icontains': search}) |
                    Q(**{'communication_type__icontains': search}) |
                    Q(**{'code__icontains': search}) |
                    Q(**{'address__icontains': search})
            )

        forward_to_portals = ForwardToPortal.objects.filter(q).order_by('id')
        context['forward_to_portals'] = forward_to_portals

        items_per_page = 50
        paginator = Paginator(forward_to_portals, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/forward-to-portal/forward-to-portal-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='forward_to_portal', allowed_actions='read')
    def detail(self, request, forward_to_portal_id, *args, **kwargs):
        try:
            forward_to_portal = ForwardToPortal.objects.get(id=forward_to_portal_id)
            context = {'page_title': f'اطلاعات انتقال دهنده *{forward_to_portal.code}*',
                       'forward_to_portal': forward_to_portal, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/portal/forward-to-portal/forward-to-portal-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='forward_to_portal', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست انتقال دهندگان شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'name__icontains': search}) |
                    Q(**{'communication_type__icontains': search}) |
                    Q(**{'code__icontains': search}) |
                    Q(**{'address__icontains': search})
            )
        forward_to_portals = ForwardToPortal.objects.filter(q).order_by('id')
        context['forward_to_portals'] = forward_to_portals

        items_per_page = 50
        paginator = Paginator(forward_to_portals, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/forward-to-portal/forward-to-portal-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='forward_to_portal', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت انتقال دهنده جدید', 'get_params': request.GET.urlencode()}

        name = fetch_data_from_http_post(request, 'name', context)
        communication_type = fetch_data_from_http_post(request, 'communication_type', context)
        code = fetch_data_from_http_post(request, 'code', context)
        address = fetch_data_from_http_post(request, 'address', context)
        price = fetch_data_from_http_post(request, 'price', context)

        if not name:
            context['err'] = 'نام بدرستی وارد نشده است'
            return render(request, 'panel/portal/forward-to-portal/forward-to-portal-list.html', context)
        if not communication_type:
            context['err'] = 'نوع ارتباط بدرستی وارد نشده است'
            return render(request, 'panel/portal/forward-to-portal/forward-to-portal-list.html', context)
        if not code:
            context['err'] = 'کد بدرستی وارد نشده است'
            return render(request, 'panel/portal/forward-to-portal/forward-to-portal-list.html', context)
        if not address:
            context['err'] = 'آدرس بدرستی وارد نشده است'
            return render(request, 'panel/portal/forward-to-portal/forward-to-portal-list.html', context)
        if not price:
            context['err'] = 'قیمت بدرستی وارد نشده است'
            return render(request, 'panel/portal/forward-to-portal/forward-to-portal-list.html', context)

        try:
            ForwardToPortal.objects.get(code=code)
            context['err'] = f'انتقال دهنده با کد {code} از قبل موجود است'
        except:
            ForwardToPortal.objects.create(
                name=name,
                communication_type=communication_type,
                code=code,
                address=address,
                price=price,
                created_by=request.user,
                updated_by=request.user,
                is_active=True,
            )
            context['message'] = f'انتقال دهنده با شناسه یکتا {code} ایجاد گردید'
        return redirect('panel:forward-to-portal-list')

    @CheckLogin()
    @CheckPermissions(section='forward_to_portal', allowed_actions='modify')
    def modify(self, request, forward_to_portal_id, *args, **kwargs):
        try:
            forward_to_portal = ForwardToPortal.objects.get(id=forward_to_portal_id)
            context = {'page_title': f'ویرایش اطلاعات انتقال دهنده *{forward_to_portal.code}*',
                       'forward_to_portal': forward_to_portal, 'get_params': request.GET.urlencode()}
            if request.method == 'GET':
                return render(request, 'panel/portal/forward-to-portal/forward-to-portal-edit.html', context)
            else:
                name = fetch_data_from_http_post(request, 'name', context, False)
                communication_type = fetch_data_from_http_post(request, 'communication_type', context, False)
                address = fetch_data_from_http_post(request, 'address', context, False)
                price = fetch_data_from_http_post(request, 'price', context, False)
                is_active = fetch_data_from_http_post(request, 'is_active', context, False)

                if name:
                    forward_to_portal.name = name
                if communication_type:
                    forward_to_portal.communication_type = communication_type
                if address:
                    forward_to_portal.address = address
                if price:
                    forward_to_portal.price = price
                if is_active == 'true':
                    forward_to_portal.is_active = True
                else:
                    forward_to_portal.is_active = False

                forward_to_portal.save()
                context['message'] = f'دریافت کننده با کد {forward_to_portal.code} ویرایش گردید'
                return redirect(
                    reverse('panel:forward-to-portal-modify-with-id',
                            kwargs={'forward_to_portal_id': forward_to_portal_id}) + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='forward_to_portal', allowed_actions='delete')
    def delete(self, request, forward_to_portal_id, *args, **kwargs):
        try:
            forward_to_portal = ForwardToPortal.objects.get(id=forward_to_portal_id)
            context = {'page_title': f'حذف انتقال دهنده {forward_to_portal.code}',
                       'get_params': request.GET.urlencode()}
            forward_to_portal.delete()
            return redirect(reverse('panel:receiver-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='forward_to_portal', allowed_actions='modify')
    def change_state(self, request, forward_to_portal_id, *args, **kwargs):
        try:
            forward_to_portal = ForwardToPortal.objects.get(id=forward_to_portal_id)
            context = {'page_title': f'تغییر وضعیت انتقال دهنده {forward_to_portal.code}',
                       'get_params': request.GET.urlencode()}
            if forward_to_portal.is_active:
                forward_to_portal.is_active = False
                forward_to_portal_is_active = 'false'
            else:
                forward_to_portal.is_active = True
                forward_to_portal_is_active = 'true'
            forward_to_portal.save()
            return JsonResponse({"forward_to_portal_is_active": forward_to_portal_is_active})
        except:
            return render(request, 'panel/err/err-not-found.html')


class CommunicationChannelView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='communication_channel', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست کانال های ارتباطی', 'get_params': request.GET.urlencode()}

        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست کانال های ارتباطی شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'name__icontains': search}) |
                    Q(**{'communication_type__icontains': search}) |
                    Q(**{'code__icontains': search}) |
                    Q(**{'phone_number__icontains': search})
            )

        communication_channels = CommunicationChannel.objects.filter(q).order_by('id')
        context['communication_channels'] = communication_channels

        items_per_page = 50
        paginator = Paginator(communication_channels, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/communication-channel/communication-channel-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='communication_channel', allowed_actions='read')
    def detail(self, request, communication_channel_id, *args, **kwargs):
        try:
            communication_channel = CommunicationChannel.objects.get(id=communication_channel_id)
            context = {'page_title': f'اطلاعات کانال ارتباطی *{communication_channel.code}*',
                       'communication_channel': communication_channel, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/portal/communication-channel/communication-channel-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='communication_channel', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست کانال های ارتباطی شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'name__icontains': search}) |
                    Q(**{'communication_type__icontains': search}) |
                    Q(**{'code__icontains': search}) |
                    Q(**{'phone_number__icontains': search})
            )
        communication_channels = CommunicationChannel.objects.filter(q).order_by('id')
        context['communication_channels'] = communication_channels

        items_per_page = 50
        paginator = Paginator(communication_channels, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/communication-channel/communication-channel-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='communication_channel', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت کانال ارتباطی جدید', 'get_params': request.GET.urlencode()}

        name = fetch_data_from_http_post(request, 'name', context)
        communication_type = fetch_data_from_http_post(request, 'communication_type', context)
        code = fetch_data_from_http_post(request, 'code', context)
        phone_number = fetch_data_from_http_post(request, 'phone_number', context)
        price = fetch_data_from_http_post(request, 'price', context)

        if not name:
            context['err'] = 'نام بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)
        if not communication_type:
            context['err'] = 'نوع ارتباط بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)
        if not code:
            context['err'] = 'کد بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)
        if not phone_number:
            context['err'] = 'شماره بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)
        if not price:
            context['err'] = 'قیمت بدرستی وارد نشده است'
            return render(request, 'panel/portal/reseller-network/reseller-network-list.html', context)

        try:
            CommunicationChannel.objects.get(code=code)
            context['err'] = f'کانال ارتباطی با کد {code} از قبل موجود است'
        except:
            CommunicationChannel.objects.create(
                name=name,
                communication_type=communication_type,
                code=code,
                phone_number=phone_number,
                price=price,
                is_active=True,
            )
            context['message'] = f'کانال ارتباطی با شناسه یکتا {code} ایجاد گردید'

        return redirect('panel:communication-channel-list')

    @CheckLogin()
    @CheckPermissions(section='communication_channel', allowed_actions='modify')
    def modify(self, request, communication_channel_id, *args, **kwargs):
        try:
            communication_channel = CommunicationChannel.objects.get(id=communication_channel_id)
            context = {'page_title': f'ویرایش کانال ارتباطی *{communication_channel.code}*',
                       'communication_channel': communication_channel, 'get_params': request.GET.urlencode()}
            if request.method == 'GET':
                return render(request, 'panel/portal/communication-channel/communication-channel-edit.html', context)
            else:
                name = fetch_data_from_http_post(request, 'name', context, False)
                communication_type = fetch_data_from_http_post(request, 'communication_type', context, False)
                phone_number = fetch_data_from_http_post(request, 'phone_number', context, False)
                price = fetch_data_from_http_post(request, 'price', context, False)
                is_active = fetch_data_from_http_post(request, 'is_active', context, False)

                if name:
                    communication_channel.name = name
                if communication_type:
                    communication_channel.communication_type = communication_type
                if phone_number:
                    communication_channel.phone_number = phone_number
                if price:
                    communication_channel.price = price
                if is_active == 'true':
                    communication_channel.is_active = True
                else:
                    communication_channel.is_active = False

                communication_channel.save()
                context['message'] = f'کانال ارتباطی با کد {communication_channel.code} ویرایش گردید'
                return redirect(
                    reverse('panel:communication-channel-modify-with-id',
                            kwargs={
                                'communication_channel_id': communication_channel_id}) + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='communication_channel', allowed_actions='delete')
    def delete(self, request, communication_channel_id, *args, **kwargs):
        try:
            communication_channel = CommunicationChannel.objects.get(id=communication_channel_id)
            context = {'page_title': f'حذف کانال ارتباطی {communication_channel.code}',
                       'get_params': request.GET.urlencode()}
            communication_channel.delete()
            return redirect(reverse('panel:communication-channel-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='communication_channel', allowed_actions='modify')
    def change_state(self, request, communication_channel_id, *args, **kwargs):
        try:
            communication_channel = CommunicationChannel.objects.get(id=communication_channel_id)
            context = {'page_title': f'تغییر وضعیت شبکه ارتباطی {communication_channel.code}',
                       'get_params': request.GET.urlencode()}
            if communication_channel.is_active:
                communication_channel.is_active = False
                communication_channel_is_active = 'false'
            else:
                communication_channel.is_active = True
                communication_channel_is_active = 'true'
            communication_channel.save()
            return JsonResponse({"communication_channel_is_active": communication_channel_is_active})
        except:
            return render(request, 'panel/err/err-not-found.html')


class RegistrarView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست تخصیص دهنده ها', 'get_params': request.GET.urlencode()}

        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست تخصیص دهنده ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'name__icontains': search}) |
                    Q(**{'register_type__icontains': search}) |
                    Q(**{'code__icontains': search})
            )

        registrars = Registrar.objects.filter(q).order_by('-created_at')
        context['registrars'] = registrars

        items_per_page = 50
        paginator = Paginator(registrars, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/registrar/registrar-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='read')
    @RequireMethod(allowed_method='POST')
    def detail(self, request, *args, **kwargs):
        context = {}
        registrar_id = fetch_data_from_http_post(request, 'registrar_id', context)
        try:
            registrar = Registrar.objects.filter(id=registrar_id)
            serializer = RegistrarSerializer(registrar, many=True)
            json_response_body = {
                "method": "post",
                "request": f"دیتای تخصیص دهنده با ایدی {registrar_id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'failed'})

    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست تخصیص دهندگان شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'name__icontains': search}) |
                    Q(**{'registrar_type__icontains': search}) |
                    Q(**{'code__icontains': search})
            )

        registrars = Registrar.objects.filter(q).order_by('-created_at')
        context['registrars'] = registrars

        items_per_page = 50
        paginator = Paginator(registrars, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/registrar/registrar-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت تخصیص دهنده جدید', 'get_params': request.GET.urlencode()}

        name = fetch_data_from_http_post(request, 'name', context)
        registrar_type = fetch_data_from_http_post(request, 'registrar_type', context)
        code = fetch_data_from_http_post(request, 'code', context)

        if not name:
            context['err'] = 'نام بدرستی وارد نشده است'
            return render(request, 'panel/portal/registrar/registrar-list.html', context)
        if not registrar_type:
            context['err'] = 'نوع تخصیص دهنده بدرستی وارد نشده است'
            return render(request, 'panel/portal/registrar/registrar-list.html', context)
        if not code:
            context['err'] = 'کد بدرستی وارد نشده است'
            return render(request, 'panel/portal/registrar/registrar-list.html', context)

        try:
            Registrar.objects.get(code=code)
            context['err'] = f'تخصیص دهنده با کد {code} از قبل موجود است'
        except:
            Registrar.objects.create(
                name=name,
                registrar_type=registrar_type,
                code=code,
                created_by=request.user,
                updated_by=request.user,
                is_active=True,
            )
            context['message'] = f'تخصیصی دهنده با شناسه یکتا {code} ایجاد گردید'

        return redirect('resource:registrar-list')

    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def modify(self, request, *args, **kwargs):
        context = {}
        registrar_id = fetch_data_from_http_post(request, 'registrar_id', context)
        try:
            registrar = Registrar.objects.get(id=registrar_id)
            context = {'page_title': f'ویرایش تخصیص دهنده با ایدی *{registrar_id}*',
                       'registrar': registrar, 'get_params': request.GET.urlencode()}
            name = fetch_data_from_http_post(request, 'fr_form_registrar_data_name', context, False)
            registrar_type = fetch_data_from_http_post(request, 'fr_form_registrar_data_registrar_type', context)
            is_active = fetch_data_from_http_post(request, 'fr_form_registrar_data_is_active', context, False)

            if name:
                registrar.name = name
            if registrar_type:
                registrar.registrar_type = registrar_type
            if is_active == 'true':
                registrar.is_active = True
            else:
                registrar.is_active = False
            registrar.save()

            return JsonResponse({'message': f'تخصیص دهنده با آیدی {registrar_id} ویرایش گردید'})
        except:
            return JsonResponse({'message': f'registrar not found'})

    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='delete')
    def delete(self, request, registrar_id, *args, **kwargs):
        try:
            registrar = Registrar.objects.get(id=registrar_id)
            context = {'page_title': f'حذف تخصیص دهنده {registrar.code}', 'get_params': request.GET.urlencode()}
            registrar.delete()
            return redirect(reverse('resource:registrar-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='registrar', allowed_actions='modify')
    def change_state(self, request, *args, **kwargs):
        context = {}
        registrar_id = fetch_data_from_http_post(request, 'registrar_id', context)
        try:
            registrar = Registrar.objects.get(id=registrar_id)
            context = {'page_title': f'تغییر وضعیت تخصیص دهنده {registrar.code}',
                       'get_params': request.GET.urlencode()}
            if registrar.is_active:
                registrar.is_active = False
                registrar_is_active = 'false'
            else:
                registrar.is_active = True
                registrar_is_active = 'true'
            registrar.save()
            return JsonResponse({"registrar_is_active": registrar_is_active})
        except:
            return render(request, 'panel/err/err-not-found.html')
