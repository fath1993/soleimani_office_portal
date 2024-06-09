from django import template
from django.db.models import Q

from automation.models import report_requested_product_processing_cancel_number, RequestedProductProcessing

register = template.Library()


def check_user_is_allowed_to_reopen_sale(request, requested_product_processing_id):
    try:
        requested_product_processing = RequestedProductProcessing.objects.get(id=requested_product_processing_id)
        if report_requested_product_processing_cancel_number(requested_product_processing,
                                                             request.user.user_profile.profile_seller_profile) >= 3:
            return False
        else:
            return True
    except:
        return False

