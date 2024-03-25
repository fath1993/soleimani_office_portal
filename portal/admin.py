from django.contrib import admin

from portal.models import Product, Registrar, ForwardToPortal, CommunicationChannel, TeaserMaker, ResellerNetwork, \
    Receiver, AdvertiseContent


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'type',
        'code',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    fields = (
        'name',
        'type',
        'code',
        'weight',
        'size',
        'color',
        'images',
        'videos',
        'product_price',
        'shipping_price',
        'send_link_price',
        'packing_price',
        'seller_commission',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    @admin.display(description="تاریخ ایجاد", empty_value='???')
    def created_at_display(self, obj):
        data_time = str(obj.created_at.strftime('%Y-%m-%d - %H:%M'))
        return data_time

    @admin.display(description="تاریخ بروزرسانی", empty_value='???')
    def updated_at_display(self, obj):
        data_time = str(obj.updated_at.strftime('%Y-%m-%d - %H:%M'))
        return data_time

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change:
            instance.created_by = user
            instance.updated_by = user
        else:
            instance.updated_by = user
        instance.save()
        form.save_m2m()
        return instance


admin.site.register(TeaserMaker)
admin.site.register(ResellerNetwork)
admin.site.register(Receiver)
admin.site.register(AdvertiseContent)
admin.site.register(ForwardToPortal)
admin.site.register(CommunicationChannel)
admin.site.register(Registrar)
