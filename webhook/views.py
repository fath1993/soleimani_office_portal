import json
import random

import jdatetime
from django.contrib.auth.models import User
from django.http import JsonResponse

from accounts.models import Profile, SellerProfile
from automation.models import ProductRelation, RequestedProduct, Customer, RequestedProductProcessing
from panel.custom_decorator import RequireMethod
from utilities.http_metod import fetch_data_from_http_post


class WebhookView:
    def __init__(self):
        super().__init__()

    @RequireMethod(allowed_method='POST')
    def webhook_request(self, request, *args, **kwargs):
        context = {'page_title': 'درخواست محصول'}

        front_input = json.loads(request.body)

        try:
            related_product_number = int(front_input['related_product_number'])
            requesting_person_phone_number = front_input['requesting_person_phone_number']
            receiving_request_phone_number = front_input['receiving_request_phone_number']
        except:
            return JsonResponse({'message': 'wrong input'})

        try:
            product_relation = ProductRelation.objects.get(receiver__receiver_phone_number=receiving_request_phone_number, number=related_product_number)

            try:
                customer = Customer.objects.get(phone_number=requesting_person_phone_number)
            except:
                customer = Customer.objects.create(
                    phone_number=requesting_person_phone_number,
                )
            customer.desired_product.add(product_relation.product)
            try:
                requested_product = RequestedProduct.objects.get(product=product_relation.product,
                                                                 customer=customer, is_processed=False)
                return JsonResponse({'message': 'too many request'})
            except:
                requested_product = RequestedProduct.objects.create(
                    product=product_relation.product,
                    customer=customer,
                )
                if product_relation.product.product_product_warehouse.available_number > 0:
                    requested_product.is_product_available_at_warehouse = True
                    requested_product.is_processed = False
                    requested_product.save()

                    sales_allowed_profiles = SellerProfile.objects.filter(daily_allowed_product_processing_number__gte=0)
                    sales_allowed_profiles_with_available_quantity = []
                    for sales_allowed_profile in sales_allowed_profiles:
                        now = jdatetime.datetime.now()
                        start_of_today = jdatetime.datetime(year=now.year, month=now.month, day=now.day, hour=0,
                                                            minute=0, second=0)
                        all_request_product_processing_that_belong_to_user = RequestedProductProcessing.objects.filter(
                            created_at__gte=start_of_today, seller=sales_allowed_profile)
                        if all_request_product_processing_that_belong_to_user.count() < sales_allowed_profile.daily_allowed_product_processing_number:
                            sales_allowed_profiles_with_available_quantity.append(sales_allowed_profile)
                    if len(sales_allowed_profiles_with_available_quantity) > 0:
                        seller = random.choice(sales_allowed_profiles_with_available_quantity)
                        RequestedProductProcessing.objects.create(
                            requested_product=requested_product,
                            seller=seller,
                            updated_by=seller,
                        )
                        return JsonResponse({'message': 'the request has been assigned.'})
                    else:
                        return JsonResponse({'message': 'no available candidate. the request is pending...'})

                else:
                    requested_product.is_product_available_at_warehouse = False
                    requested_product.is_processed = True
                    requested_product.save()
                    return JsonResponse({'message': 'product not available at the moment. scheduled'})

        except Exception as e:
            print(e)
            return JsonResponse({'message': 'not found'})


