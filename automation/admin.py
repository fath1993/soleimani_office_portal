from django.contrib import admin

from automation.models import CreditCard, RequestedProductProcessing, Customer, RequestedProduct, \
    RequestedProductProcessingReport

admin.site.register(CreditCard)
admin.site.register(Customer)
admin.site.register(RequestedProduct)
admin.site.register(RequestedProductProcessing)
admin.site.register(RequestedProductProcessingReport)
