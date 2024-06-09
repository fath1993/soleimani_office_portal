from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import WarehouseProfile, Profile
from automation.models import RequestedProductProcessing, create_requested_product_processing_report, \
    RequestedProductProcessingReport, pick_seller, pick_warehouse_keeper, pick_delivery_man, Customer, \
    create_requested_product_processing_cancel_report, report_requested_product_processing_cancel_number, CreditCard, \
    ProductRelation, ProductWarehouse
from gallery.models import FileGallery
from accounts.custom_decorator import CheckLogin, CheckPermissions, RequireMethod
from automation.serializer import RequestedProductProcessingReportSerializer, ProductSerializer, CustomerSerializer, \
    CreditCardSerializer, ProductRelationSerializer, ProductWarehouseSerializer
from resource.models import Product, Receiver
from utilities.http_metod import fetch_data_from_http_post, fetch_files_from_http_post_data, fetch_data_from_http_get, \
    fetch_data_list_from_http_post


class ProductRelationView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='product_relation', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست ارتباطات محصولات و دریافت کنندگان', 'get_params': request.GET.urlencode(), 'err': request.GET.get('err', None), 'message': request.GET.get('message', None)}

        product_relations = ProductRelation.objects.filter().order_by('-created_at')
        context['product_relations'] = product_relations

        items_per_page = 50
        paginator = Paginator(product_relations, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/product-relation/product-relation-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='product_relation', allowed_actions='read')
    @RequireMethod(allowed_method='POST')
    def detail(self, request, *args, **kwargs):
        context = {}
        product_relation_id = fetch_data_from_http_post(request, 'product_relation_id', context)
        try:
            product_relation = ProductRelation.objects.filter(id=product_relation_id)
            serializer = ProductRelationSerializer(product_relation, many=True)
            json_response_body = {
                "method": "post",
                "request": f"دیتای ارتباط محصول و دریافت کننده با شناسه یکتای {product_relation_id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'failed'})

    @CheckLogin()
    @CheckPermissions(section='product_relation', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست ارتباطات محصولات و دریافت کنندگان شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'number__icontains': search}) |
                    Q(**{'product__name__icontains': search}) |
                    Q(**{'receiver__name__icontains': search})
            )
        product_relations = ProductRelation.objects.filter(q).order_by('-created_at')
        context['product_relations'] = product_relations

        items_per_page = 50
        paginator = Paginator(product_relations, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/product-relation/product-relation-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='product_relation', allowed_actions='create')
    @RequireMethod(allowed_method='POST')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت ارتباط محصول و دریافت کننده جدید', 'get_params': request.GET.urlencode()}

        product_id = fetch_data_from_http_post(request, 'product_id', context)
        receiver_id = fetch_data_from_http_post(request, 'receiver_id', context)
        number = fetch_data_from_http_post(request, 'number', context)

        if not product_id:
            err = 'محصول بدرستی وارد نشده است'
            return redirect(reverse('automation:product-relation-list') + f'?err={err}')
        else:
            try:
                product = Product.objects.get(id=product_id)
            except:
                err = 'محصول بدرستی وارد نشده است'
                return redirect(reverse('automation:product-relation-list') + f'?err={err}')
        if not receiver_id:
            err = 'دریافت کننده بدرستی وارد نشده است'
            return redirect(reverse('automation:product-relation-list') + f'?err={err}')
        else:
            try:
                receiver = Receiver.objects.get(id=receiver_id)
            except:
                err = 'دریافت کننده بدرستی وارد نشده است'
                return redirect(reverse('automation:product-relation-list') + f'?err={err}')
        if not number:
            err = 'شماره بدرستی وارد نشده است'
            return redirect(reverse('automation:product-relation-list') + f'?err={err}')

        try:
            ProductRelation.objects.get(receiver__id=receiver_id, number=number)
            err = f'  و ارتباط کد دریافت کننده {receiver_id} و عدد {number} وجود دارد'
            return redirect(reverse('automation:product-relation-list') + f'?err={err}')
        except:
            ProductRelation.objects.create(
                product=product,
                receiver=receiver,
                number=number,
                created_by=request.user,
            )

            message = f'ارتباط با کد محصول {product_id} و کد دریافت کننده {receiver_id} و عدد {number} ایجاد گردید'
            return redirect(reverse('automation:product-relation-list') + f'?message={message}')

    @CheckLogin()
    @CheckPermissions(section='product_relation', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def modify(self, request, *args, **kwargs):
        context = {}
        product_relation_id = fetch_data_from_http_post(request, 'product_relation_id', context)
        try:
            product_relation = ProductRelation.objects.get(id=product_relation_id)
            context = {'page_title': f'ویرایش ارتباط محصول و دریافت کننده با شناسه یکتای *{product_relation_id}*',
                       'product_relation': product_relation, 'get_params': request.GET.urlencode()}
            product_id = fetch_data_from_http_post(request, 'fpr_form_modal_product_relation_data_product_id', context)
            receiver_id = fetch_data_from_http_post(request, 'fpr_form_modal_product_relation_data_receiver_id', context)
            number = fetch_data_from_http_post(request, 'fpr_form_modal_product_relation_data_number', context)

            if not product_id:
                err = 'محصول بدرستی وارد نشده است'
                return JsonResponse({'message': f'{err}'})
            else:
                try:
                    product = Product.objects.get(id=product_id)
                except:
                    err = 'محصول بدرستی وارد نشده است'
                    return JsonResponse({'message': f'{err}'})
            if not receiver_id:
                err = 'دریافت کننده بدرستی وارد نشده است'
                return JsonResponse({'message': f'{err}'})
            else:
                try:
                    receiver = Receiver.objects.get(id=receiver_id)
                except:
                    err = 'دریافت کننده بدرستی وارد نشده است'
                    return JsonResponse({'message': f'{err}'})
            try:
                ProductRelation.objects.get(receiver__id=receiver_id, number=number)
                err = f'ارتباط کد دریافت کننده {receiver_id} و عدد {number} وجود دارد'
                return JsonResponse({'message': f'{err}', 'err': True})
            except:
                product_relation.product = product
                product_relation.receiver = receiver
                product_relation.number = number
                product_relation.save()

            return JsonResponse({'message': f'ارتباط محصول و دریافت کننده با شناسه یکتا {product_relation_id} ویرایش گردید'})
        except:
            return JsonResponse({'message': f'product relation not found'})

    @CheckLogin()
    @CheckPermissions(section='product_relation', allowed_actions='delete')
    def delete(self, request, product_relation_id, *args, **kwargs):
        try:
            product_relation = ProductRelation.objects.get(id=product_relation_id)
            context = {'page_title': f'حذف ارتباط محصول و دریافت کننده با شناسه یکتای {product_relation_id}', 'get_params': request.GET.urlencode()}
            product_relation.delete()
            return redirect(reverse('automation:product-relation-list') + f'?{request.GET.urlencode()}')
        except Exception as e:
            print(e)
            return render(request, 'panel/err/err-not-found.html')


class ProductWarehouseView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='warehouse', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست محصولات', 'get_params': request.GET.urlencode(),
                   'err': request.GET.get('err', None), 'message': request.GET.get('message', None)}

        product_warehouse = ProductWarehouse.objects.filter().order_by('-created_at')
        context['product_warehouse'] = product_warehouse

        items_per_page = 50
        paginator = Paginator(product_warehouse, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/product-warehouse/product-warehouse-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='warehouse', allowed_actions='read')
    @RequireMethod(allowed_method='POST')
    def detail(self, request, *args, **kwargs):
        context = {}
        product_warehouse_id = fetch_data_from_http_post(request, 'product_warehouse_id', context)
        try:
            product_warehouse = ProductWarehouse.objects.filter(id=product_warehouse_id)
            serializer = ProductWarehouseSerializer(product_warehouse, many=True)
            json_response_body = {
                "method": "post",
                "request": f"دیتای انبار محصول با ایدی {product_warehouse_id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'failed'})

    @CheckLogin()
    @CheckPermissions(section='warehouse', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست محصولات شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'product__name__icontains': search}) |
                    Q(**{'product__code__icontains': search})
            )

        product_warehouse = ProductWarehouse.objects.filter().order_by('-created_at')
        context['product_warehouse'] = product_warehouse

        items_per_page = 50
        paginator = Paginator(product_warehouse, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/product-warehouse/product-warehouse-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='warehouse', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def modify(self, request, *args, **kwargs):
        context = {}
        product_warehouse_id = fetch_data_from_http_post(request, 'product_warehouse_id', context)
        try:
            product_warehouse = ProductWarehouse.objects.get(id=product_warehouse_id)
            context = {'page_title': f'ویرایش اطلاعات انبار محصول با ایدی *{product_warehouse_id}*',
                       'product_warehouse': product_warehouse, 'get_params': request.GET.urlencode()}
            available_number = fetch_data_from_http_post(request, 'fmpw_form_modal_product_data_available_number', context)

            if available_number:
                product_warehouse.available_number = available_number

            product_warehouse.save()

            return JsonResponse({'message': f'اطلاعات انبار محصول با آیدی {product_warehouse_id} ویرایش گردید'})
        except:
            return JsonResponse({'message': f'registrar not found'})



class CreditCardView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='credit_card', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست کارت های بانکی', 'get_params': request.GET.urlencode()}

        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست کارت های بانکی شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'bank_name__icontains': search}) |
                    Q(**{'account_number__icontains': search}) |
                    Q(**{'card_number__icontains': search}) |
                    Q(**{'isbn__icontains': search})
            )

        credit_cards = CreditCard.objects.filter(q).order_by('id')
        context['credit_cards'] = credit_cards

        items_per_page = 50
        paginator = Paginator(credit_cards, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/credit-card/credit-card-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='credit_card', allowed_actions='read')
    @RequireMethod(allowed_method='POST')
    def detail(self, request, *args, **kwargs):
        context = {}
        credit_card_id = fetch_data_from_http_post(request, 'credit_card_id', context)
        try:
            credit_cards = CreditCard.objects.filter(id=credit_card_id)
            serializer = CreditCardSerializer(credit_cards, many=True)
            json_response_body = {
                "method": "post",
                "request": f"دیتای کارت بانکی با ایدی {credit_card_id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'failed'})

    @CheckLogin()
    @CheckPermissions(section='credit_card', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست کارت های بانکی شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'bank_name__icontains': search}) |
                    Q(**{'account_number__icontains': search}) |
                    Q(**{'card_number__icontains': search}) |
                    Q(**{'isbn__icontains': search})
            )

        credit_cards = CreditCard.objects.filter(q).order_by('id')
        context['credit_cards'] = credit_cards

        items_per_page = 50
        paginator = Paginator(credit_cards, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/credit-card/credit-card-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='credit_card', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت کارت بانکی جدید', 'get_params': request.GET.urlencode()}

        bank_name = fetch_data_from_http_post(request, 'bank_name', context)
        account_number = fetch_data_from_http_post(request, 'account_number', context)
        card_number = fetch_data_from_http_post(request, 'card_number', context)
        isbn = fetch_data_from_http_post(request, 'isbn', context)
        owner_id = fetch_data_from_http_post(request, 'owner_id', context)
        brokers = fetch_data_list_from_http_post(request, 'brokers', context)

        if not bank_name:
            context['err'] = 'نام بانک بدرستی وارد نشده است'
            return render(request, 'panel/portal/registrar/registrar-list.html', context)
        if not account_number:
            context['err'] = 'شماره حساب بدرستی وارد نشده است'
            return render(request, 'panel/portal/registrar/registrar-list.html', context)
        if not card_number:
            context['err'] = 'شماره کارت بدرستی وارد نشده است'
            return render(request, 'panel/portal/registrar/registrar-list.html', context)
        if not isbn:
            context['err'] = 'شماره شبا بدرستی وارد نشده است'
            return render(request, 'panel/portal/registrar/registrar-list.html', context)
        if not owner_id:
            context['err'] = 'مالک کارت بدرستی وارد نشده است'
            return render(request, 'panel/portal/registrar/registrar-list.html', context)
        else:
            try:
                owner = Profile.objects.get(id=owner_id)
            except:
                context['err'] = 'مالک کارت بدرستی وارد نشده است'
                return render(request, 'panel/portal/registrar/registrar-list.html', context)
        try:
            CreditCard.objects.get(account_number=account_number, card_number=card_number)
            context['err'] = f'کارت بانکی {card_number} با شماره حساب {account_number} از قبل موجود است'
        except:
            new_credit_card = CreditCard.objects.create(
                bank_name=bank_name,
                account_number=account_number,
                card_number=card_number,
                isbn=isbn,
                owner=owner,
                created_by=request.user,
                updated_by=request.user,
                is_active=True,
            )
            for profile_id in brokers:
                try:
                    broker = Profile.objects.get(id=profile_id)
                    new_credit_card.brokers.add(broker)
                except:
                    pass

            context['message'] = f'کارت بانکی {card_number} با شماره حساب {account_number} ایجاد گردید'

        return redirect('automation:credit-card-list')

    @CheckLogin()
    @CheckPermissions(section='credit_card', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def modify(self, request, *args, **kwargs):
        context = {}
        credit_card_id = fetch_data_from_http_post(request, 'credit_card_id', context)
        try:
            credit_card = CreditCard.objects.get(id=credit_card_id)
            context = {'page_title': f'ویرایش کارت بانکی *{credit_card.card_number}*',
                       'credit_card': credit_card, 'get_params': request.GET.urlencode()}
            bank_name = fetch_data_from_http_post(request, 'fcc_form_credit_card_data_bank_name', context, False)
            account_number = fetch_data_from_http_post(request, 'fcc_form_credit_card_data_account_number', context)
            card_number = fetch_data_from_http_post(request, 'fcc_form_credit_card_data_card_number', context)
            isbn = fetch_data_from_http_post(request, 'fcc_form_credit_card_data_isbn', context, False)
            owner_id = fetch_data_from_http_post(request, 'fcc_form_credit_card_data_owner_id', context, False)
            brokers = fetch_data_list_from_http_post(request, 'fcc_form_credit_card_data_brokers', context, False)
            is_active = fetch_data_from_http_post(request, 'fcc_form_credit_card_data_is_active', context)

            if bank_name:
                credit_card.bank_name = bank_name
            if account_number:
                credit_card.account_number = account_number
            if card_number:
                credit_card.card_number = card_number
            if isbn:
                credit_card.isbn = isbn
            if owner_id:
                try:
                    credit_card.owner_id = Profile.objects.get(id=owner_id)
                except:
                    pass
            if is_active == 'true':
                credit_card.is_active = True
            else:
                credit_card.is_active = False
            credit_card.save()

            credit_card.brokers.clear()
            if brokers:
                for profile_id in brokers:
                    try:
                        broker = Profile.objects.get(id=profile_id)
                        credit_card.brokers.add(broker)
                    except:
                        pass

            return JsonResponse({'message': f'کارت بانکی {card_number} با شماره حساب {account_number} ویرایش گردید'})
        except:
            return JsonResponse({'message': f'credit card not found'})

    @CheckLogin()
    @CheckPermissions(section='credit_card', allowed_actions='delete')
    def delete(self, request, credit_card_id, *args, **kwargs):
        try:
            credit_card = CreditCard.objects.get(id=credit_card_id)
            context = {'page_title': f'حذف کارت بانکی {credit_card.card_number}', 'get_params': request.GET.urlencode()}
            credit_card.delete()
            return redirect(reverse('automation:credit-card-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='credit_card', allowed_actions='modify')
    def change_state(self, request, credit_card_id, *args, **kwargs):
        try:
            credit_card = CreditCard.objects.get(id=credit_card_id)
            context = {'page_title': f'تغییر وضعیت کارت بانکی {credit_card.card_number}', 'get_params': request.GET.urlencode()}
            if credit_card.is_active:
                credit_card.is_active = False
                credit_card_is_active = 'false'
            else:
                credit_card.is_active = True
                credit_card_is_active = 'true'
            credit_card.save()
            return JsonResponse({"credit_card_is_active": credit_card_is_active})
        except:
            return render(request, 'panel/err/err-not-found.html')


class CustomerView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='customer', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست مشتری ها', 'get_params': request.GET.urlencode()}

        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست مشتری ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'phone_number__icontains': search}) |
                    Q(**{'full_name__icontains': search}) |
                    Q(**{'age__icontains': search}) |
                    Q(**{'address__icontains': search})
            )

        customers = Customer.objects.filter(q).order_by('id')
        context['customers'] = customers

        items_per_page = 50
        paginator = Paginator(customers, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/customer/customer-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='customer', allowed_actions='read')
    @RequireMethod(allowed_method='POST')
    def detail(self, request, *args, **kwargs):
        context = {}
        customer_id = fetch_data_from_http_post(request, 'customer_id', context)
        try:
            customer = Customer.objects.filter(id=customer_id)
            serializer = CustomerSerializer(customer, many=True)
            json_response_body = {
                "method": "post",
                "request": f"دیتای مشتری با ایدی {customer_id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'failed'})

    @CheckLogin()
    @CheckPermissions(section='customer', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست مشتری ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                    Q(**{'phone_number__icontains': search}) |
                    Q(**{'full_name__icontains': search}) |
                    Q(**{'age__icontains': search}) |
                    Q(**{'address__icontains': search})
            )

        customers = Customer.objects.filter(q).order_by('id')
        context['customers'] = customers

        items_per_page = 50
        paginator = Paginator(customers, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/portal/customer/customer-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='customer', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def modify(self, request, *args, **kwargs):
        context = {}
        customer_id = fetch_data_from_http_post(request, 'customer_id', context)
        try:
            customer = Customer.objects.get(id=customer_id)
            context = {'page_title': f'ویرایش مشتری *{customer.phone_number}*',
                       'customer': customer, 'get_params': request.GET.urlencode()}
            phone_number = fetch_data_from_http_post(request, 'fc_form_customer_data_phone_number', context, False)
            full_name = fetch_data_from_http_post(request, 'fc_form_customer_data_full_name', context)
            age = fetch_data_from_http_post(request, 'fc_form_customer_data_age', context)
            address = fetch_data_from_http_post(request, 'fc_form_customer_data_address', context, False)

            if phone_number:
                customer.phone_number = phone_number
            if full_name:
                customer.full_name = full_name
            if age:
                customer.age = age
            if address:
                customer.address = address
            customer.save()

            return JsonResponse({'message': f'مشتری با شماره {phone_number} ویرایش گردید', 'new_title': f'{phone_number}'})
        except:
            return JsonResponse({'message': f'customer not found'})

    @CheckLogin()
    @CheckPermissions(section='customer', allowed_actions='delete')
    def delete(self, request, customer_id, *args, **kwargs):
        try:
            customer = Customer.objects.get(id=customer_id)
            context = {'page_title': f'حذف مشتری با شماره همراه {customer.phone_number}', 'get_params': request.GET.urlencode()}
            customer.delete()
            return redirect(reverse('automation:customer-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')


class RequestedProductProcessingView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    def admin_list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست پردازش همه سفارش ها', 'get_params': request.GET.urlencode()}

        requested_product_processing = RequestedProductProcessing.objects.filter()
        context['requested_product_processing'] = requested_product_processing

        items_per_page = 50
        paginator = Paginator(requested_product_processing, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/cartable/cartable-list.html', context)

    @CheckLogin()
    def public_list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست پردازش سفارش های عمومی', 'get_params': request.GET.urlencode()}

        q = Q()

        q &= (
            Q(**{'seller__isnull': True})
        )
        q &= (
            Q(**{'sales_status': 'canceled'})
        )

        requested_product_processing = RequestedProductProcessing.objects.filter(q)
        context['requested_product_processing'] = requested_product_processing

        items_per_page = 50
        paginator = Paginator(requested_product_processing, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/cartable/cartable-list.html', context)

    @CheckLogin()
    def list(self, request, *args, **kwargs):
        context = {'page_title': f'لیست پردازش سفارش های اختصاصی فروشنده {request.user.username}',
                   'get_params': request.GET.urlencode()}

        profile = request.user.user_profile

        q = Q()
        q &= (
            Q(**{'seller__isnull': False})
        )

        if not request.user.is_superuser:
            q &= (
                    Q(**{'seller': profile.profile_seller_profile}) |
                    Q(**{'warehouse_keeper': profile.profile_warehouse_profile}) |
                    Q(**{'delivery_man': profile.profile_delivery_profile})
            )

        requested_product_processing = RequestedProductProcessing.objects.filter(q)
        context['requested_product_processing'] = requested_product_processing

        items_per_page = 50
        paginator = Paginator(requested_product_processing, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/cartable/cartable-list.html', context)

    @CheckLogin()
    def filter(self, request, *args, **kwargs):
        context = {}
        search = fetch_data_from_http_get(request, 'search', context)
        filter_department_state = fetch_data_from_http_get(request, 'filter_department_state', context)
        filter_sale_state = fetch_data_from_http_get(request, 'filter_sale_state', context)
        filter_warehouse_state = fetch_data_from_http_get(request, 'filter_warehouse_state', context)
        filter_delivery_state = fetch_data_from_http_get(request, 'filter_delivery_state', context)

        profile = request.user.user_profile

        q = Q()
        page_title = f''''''

        if not request.user.is_superuser:
            q &= (
                    Q(**{'seller': profile.profile_seller_profile}) |
                    Q(**{'warehouse_keeper': profile.profile_warehouse_profile}) |
                    Q(**{'delivery_man': profile.profile_delivery_profile})
            )

        if search:
            page_title += f'search: {search}, '
            q &= (
                    Q(**{'id__icontains': search}) |
                    Q(**{'requested_product__customer__phone_number__icontains': search}) |
                    Q(**{'requested_product__product__name__icontains': search})
            )

        if filter_department_state:
            page_title += f'in_department_status: {filter_department_state}, '
            q &= (
                Q(**{'in_department_status': filter_department_state})
            )

        if filter_sale_state:
            page_title += f'sales_status: {filter_sale_state}, '
            q &= (
                Q(**{'sales_status': filter_sale_state})
            )
        if filter_warehouse_state:
            page_title += f'warehouse_status: {filter_warehouse_state}, '
            q &= (
                Q(**{'warehouse_status': filter_warehouse_state})
            )
        if filter_delivery_state:
            page_title += f'delivery_status: {filter_delivery_state}, '
            q &= (
                Q(**{'delivery_status': filter_delivery_state})
            )
        context['page_title'] = f'لیست پردازش سفارش های اختصاصی شامل *{page_title}*'
        context['get_params'] = request.GET.urlencode()

        requested_product_processing = RequestedProductProcessing.objects.filter(q)
        context['requested_product_processing'] = requested_product_processing

        items_per_page = 50
        paginator = Paginator(requested_product_processing, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/cartable/cartable-list.html', context)

    @CheckLogin()
    @RequireMethod(allowed_method='POST')
    def overall_data(self, request, *args, **kwargs):
        context = {}
        requested_product_processing_id = fetch_data_from_http_post(request, 'requested_product_processing_id',
                                                                    context)
        profile = request.user.user_profile

        q = Q()
        q &= (
            Q(**{'pk': requested_product_processing_id})
        )
        if not request.user.is_superuser:
            q &= (
                    Q(**{'seller': profile.profile_seller_profile}) |
                    Q(**{'warehouse_keeper': profile.profile_warehouse_profile}) |
                    Q(**{'delivery_man': profile.profile_delivery_profile})
            )

        try:
            requested_product_processing = RequestedProductProcessing.objects.get(q)
            json_response_body = {
                "method": "post",
                "request": f"دیتای کلی پردازش محصول درخواستی با ایدی {requested_product_processing.requested_product.product.id}",
                "result": "موفق",
                "data": {
                    'customer_phone_number': f'{requested_product_processing.requested_product.customer.phone_number}',
                    'product_name': f'{requested_product_processing.requested_product.product.name}',
                    'product_link': '',
                }
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({"message": 'requested product processing not found'})

    @CheckLogin()
    @RequireMethod(allowed_method='POST')
    def product_detail(self, request, *args, **kwargs):
        context = {}
        requested_product_processing_id = fetch_data_from_http_post(request, 'requested_product_processing_id',
                                                                    context)
        profile = request.user.user_profile

        q = Q()
        q &= (
            Q(**{'pk': requested_product_processing_id})
        )
        if not request.user.is_superuser:
            q &= (
                    Q(**{'seller': profile.profile_seller_profile}) |
                    Q(**{'warehouse_keeper': profile.profile_warehouse_profile}) |
                    Q(**{'delivery_man': profile.profile_delivery_profile})
            )
        try:
            requested_product_processing = RequestedProductProcessing.objects.get(q)
            query_products = Product.objects.filter(id=requested_product_processing.requested_product.product.id)
            serializer = ProductSerializer(query_products, many=True)
            json_response_body = {
                "method": "post",
                "request": f"دیتای مجصول پردازش محصول درخواستی با ایدی {requested_product_processing.requested_product.product.id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({"message": 'requested product processing not found'})

    @CheckLogin()
    @RequireMethod(allowed_method='POST')
    def customer_detail(self, request, *args, **kwargs):
        context = {}
        requested_product_processing_id = fetch_data_from_http_post(request, 'requested_product_processing_id',
                                                                    context)
        profile = request.user.user_profile

        q = Q()
        q &= (
            Q(**{'pk': requested_product_processing_id})
        )
        if not request.user.is_superuser:
            q &= (
                    Q(**{'seller': profile.profile_seller_profile}) |
                    Q(**{'warehouse_keeper': profile.profile_warehouse_profile}) |
                    Q(**{'delivery_man': profile.profile_delivery_profile})
            )
        try:
            requested_product_processing = RequestedProductProcessing.objects.get(q)
            customers = Customer.objects.filter(id=requested_product_processing.requested_product.customer.id)
            serializer = CustomerSerializer(customers, many=True)
            json_response_body = {
                "method": "post",
                "request": f"دیتای کاربر پردازش محصول درخواستی با ایدی {requested_product_processing.id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse({"message": 'requested product processing not found'})

    @CheckLogin()
    @CheckPermissions(section='sale', allowed_actions='modify')
    @RequireMethod(allowed_method='POST')
    def modify_customer_data(self, request, *args, **kwargs):
        context = {}
        requested_product_processing_id = fetch_data_from_http_post(request, 'requested_product_processing_id', context)
        try:
            requested_product_processing = RequestedProductProcessing.objects.get(id=requested_product_processing_id)
            full_name = fetch_data_from_http_post(request, 'fc_form_customer_data_full_name',
                                                  context)

            age = fetch_data_from_http_post(request, 'fc_form_customer_data_age',
                                            context)

            address = fetch_data_from_http_post(request, 'fc_form_customer_data_address',
                                                context)
            customer = requested_product_processing.requested_product.customer
            if full_name:
                customer.full_name = full_name

            if age:
                customer.age = age

            if address:
                customer.address = address
            customer.save()

            customers = Customer.objects.filter(id=customer.id)
            serializer = CustomerSerializer(customers, many=True)
            json_response_body = {
                "method": "post",
                "message": f'اطلاعات مشتری با شماره همراه {customer.phone_number} ویرایش گردید',
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(e)
            return JsonResponse(
                {'message': f'پردازش محصول درخواستی با ایدی {requested_product_processing_id} پیدا نشد'})

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
            q &= (
                    Q(**{'seller': profile.profile_seller_profile}) |
                    Q(**{'warehouse_keeper': profile.profile_warehouse_profile}) |
                    Q(**{'delivery_man': profile.profile_delivery_profile})
            )

        try:
            requested_product_processing = RequestedProductProcessing.objects.get(q)
            requested_product_processing_reports = RequestedProductProcessingReport.objects.filter(
                requested_product_processing=requested_product_processing)
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
            mss_sold_number = fetch_data_from_http_post(request, 'mss_sold_number', context)
            mss_message = fetch_data_from_http_post(request, 'mss_message', context)

            if mss_status == 'sold':
                requested_product_processing.product_number = int(mss_sold_number)
                requested_product_processing.save()

            requested_product_processing_action(request, requested_product_processing, 'sale', mss_status, mss_message)
            return JsonResponse({"message": f'{mss_status}', 'cancel_number': (
                                                                                          requested_product_processing.cancel_multiply * 3) + requested_product_processing.cancel_number})

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

            msa_status = fetch_data_from_http_post(request, 'msa_status', context)
            msa_message = fetch_data_from_http_post(request, 'msa_message', context)

            warehouse_profiles = WarehouseProfile.objects.all()
            if warehouse_profiles.count() == 0:
                return JsonResponse({"message": 'no available warehouse keeper'})

            requested_product_processing_action(request, requested_product_processing, 'sale', msa_status, msa_message)
            return JsonResponse({"message": f'{msa_status}'})

        except Exception as e:
            print(e)
            return JsonResponse({"message": 'requested product processing not found'})

    @CheckLogin()
    @RequireMethod(allowed_method='POST')
    def reopen_sale(self, request, *args, **kwargs):
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
            mcr_status = fetch_data_from_http_post(request, 'mcr_status', context)
            mcr_message = fetch_data_from_http_post(request, 'mcr_message', context)

            if report_requested_product_processing_cancel_number(requested_product_processing, seller_profile) >= 3:
                return JsonResponse({"message": f'seller qualification error'})
            requested_product_processing_action(request, requested_product_processing, 'sale', mcr_status, mcr_message)
            return JsonResponse({"message": f'{mcr_status}'})

        except Exception as e:
            print(e)
            return JsonResponse({"message": 'requested product processing not found'})

    @CheckLogin()
    @RequireMethod(allowed_method='POST')
    def change_warehouse_state(self, request, *args, **kwargs):
        context = {}
        try:
            warehouse_profile = request.user.user_profile.profile_warehouse_profile
        except:
            return JsonResponse({"message": 'warehouse profile not found'})

        requested_product_processing_id = fetch_data_from_http_post(request, 'requested_product_processing_id',
                                                                    context)

        try:
            requested_product_processing = RequestedProductProcessing.objects.get(id=requested_product_processing_id)
            mws_status = fetch_data_from_http_post(request, 'mws_status', context)
            mws_message = fetch_data_from_http_post(request, 'mws_message', context)

            requested_product_processing_action(request, requested_product_processing, 'sale', mws_status, mws_message)
            return JsonResponse({"message": f'{mws_status}'})

        except:
            return JsonResponse({"message": 'not authorized warehouse keeper'})

    @CheckLogin()
    @RequireMethod(allowed_method='POST')
    def change_delivery_state(self, request, *args, **kwargs):
        context = {}
        try:
            delivery_profile = request.user.user_profile.profile_delivery_profile
        except:
            return JsonResponse({"message": 'delivery profile not found'})

        requested_product_processing_id = fetch_data_from_http_post(request, 'requested_product_processing_id',
                                                                    context)

        try:
            requested_product_processing = RequestedProductProcessing.objects.get(id=requested_product_processing_id)
            mds_status = fetch_data_from_http_post(request, 'mds_status', context)
            mds_message = fetch_data_from_http_post(request, 'mds_message', context)

            requested_product_processing_action(request, requested_product_processing, 'sale', mds_status, mds_message)
            return JsonResponse({"message": f'{mds_status}'})

        except:
            return JsonResponse({"message": 'not authorized delivery'})


def requested_product_processing_action(request, requested_product_processing, report_from_department, status, message):
    create_requested_product_processing_report(requested_product_processing, report_from_department, status, message,
                                               request.user)

    if status == 'sold':
        requested_product_processing.in_department_status = 'sale'
        requested_product_processing.is_confirmed_by_sales_department = False
        requested_product_processing.sales_status = 'pending_sales_approval'
        requested_product_processing.product_price = requested_product_processing.requested_product.product.product_price
        requested_product_processing.request_total_income = requested_product_processing.requested_product.product.product_price * requested_product_processing.product_number

    if status == 'canceled':
        create_requested_product_processing_cancel_report(requested_product_processing,
                                                          requested_product_processing.seller, request.user)
        requested_product_processing.in_department_status = 'sale'
        requested_product_processing.cancel_number += 1
        if requested_product_processing.cancel_number >= 3:
            requested_product_processing.seller = None
            requested_product_processing.cancel_number = 0
            requested_product_processing.cancel_multiply += 1
        requested_product_processing.is_confirmed_by_sales_department = False
        requested_product_processing.sales_status = 'canceled'
        requested_product_processing.product_price = 0
        requested_product_processing.request_total_income = 0
        requested_product_processing.product_number = 0
        requested_product_processing.warehouse_keeper = None
        requested_product_processing.warehouse_status = 'canceled'
        requested_product_processing.delivery_man = None
        requested_product_processing.delivery_status = 'canceled'

        requested_product = requested_product_processing.requested_product
        requested_product.is_processed = True
        requested_product.save()

    if status == 'confirmed':
        requested_product_processing.in_department_status = 'warehouse'
        requested_product_processing.is_confirmed_by_sales_department = True
        requested_product_processing.sales_status = 'sold'
        requested_product_processing.warehouse_keeper = pick_warehouse_keeper()
        requested_product_processing.warehouse_status = 'processing'

        current_available_product_quantity = requested_product_processing.requested_product.product.product_product_warehouse
        if (current_available_product_quantity.available_number - requested_product_processing.product_number) > 0:
            current_available_product_quantity.available_number -= requested_product_processing.product_number
        else:
            current_available_product_quantity.available_number = 0
        current_available_product_quantity.save()

    if status == 'recheck':
        requested_product_processing.in_department_status = 'sale'
        requested_product_processing.is_confirmed_by_sales_department = False
        requested_product_processing.sales_status = 'recheck'

    if status == 'change_seller':
        requested_product_processing.in_department_status = 'sale'
        requested_product_processing.is_confirmed_by_sales_department = False
        requested_product_processing.sales_status = 'change_seller'
        old_seller = requested_product_processing.seller
        requested_product_processing.seller = pick_seller(old_seller)
        requested_product_processing.sales_status = 'processing'

    if status == 'sent_to_delivery':
        requested_product_processing.in_department_status = 'delivery'
        requested_product_processing.warehouse_status = 'sent_to_delivery'
        requested_product_processing.delivery_man = pick_delivery_man()
        requested_product_processing.delivery_status = 'processing'

    if status == 'return_to_sales':
        requested_product_processing.in_department_status = 'sale'
        requested_product_processing.is_confirmed_by_sales_department = False
        requested_product_processing.sales_status = 'processing'
        requested_product_processing.warehouse_status = 'return_to_sales'

        current_available_product_quantity = requested_product_processing.requested_product.product.product_product_warehouse
        current_available_product_quantity.available_number += requested_product_processing.product_number
        current_available_product_quantity.save()

    if status == 'delivered':
        requested_product_processing.in_department_status = 'delivery'
        requested_product_processing.delivery_status = 'delivered'

        requested_product = requested_product_processing.requested_product
        requested_product.is_processed = True
        requested_product.save()

    if status == 'return_to_warehouse':
        requested_product_processing.in_department_status = 'warehouse'
        requested_product_processing.warehouse_status = 'processing'
        requested_product_processing.delivery_status = 'pending'

    if status == 'myself':
        requested_product_processing.in_department_status = 'sale'
        requested_product_processing.seller = request.user.user_profile.profile_seller_profile
        requested_product_processing.is_confirmed_by_sales_department = False
        requested_product_processing.sales_status = 'processing'
        requested_product_processing.warehouse_status = 'pending'
        requested_product_processing.delivery_status = 'pending'

    if status == 'everyone':
        requested_product_processing.in_department_status = 'sale'
        requested_product_processing.seller = None
        requested_product_processing.is_confirmed_by_sales_department = False
        requested_product_processing.sales_status = 'pending'
        requested_product_processing.warehouse_status = 'pending'
        requested_product_processing.delivery_status = 'pending'

    # requested_product_processing.in_department_status =
    # requested_product_processing.seller =
    # requested_product_processing.is_confirmed_by_sales_department =
    # requested_product_processing.sales_status =
    # requested_product_processing.cancel_number =
    # requested_product_processing.product_price =
    # requested_product_processing.request_total_income =
    # requested_product_processing.warehouse_keeper =
    # requested_product_processing.warehouse_status =
    # requested_product_processing.delivery_man =
    # requested_product_processing.delivery_status =

    requested_product_processing.updated_by = request.user

    requested_product_processing.save()
    return requested_product_processing
