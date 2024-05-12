from django.contrib import admin

from portal.models import Product, Registrar, ForwardToPortal, CommunicationChannel, TeaserMaker, ResellerNetwork, \
    Receiver, AdvertiseContent, ProductWarehouse


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

        'is_active',
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


@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'receiving_type',
        'code',
        'receiver_phone_number',
        'price',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    fields = (
        'name',
        'receiving_type',
        'code',
        'receiver_phone_number',
        'price',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',

        'is_active',
    )

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


admin.site.register(ProductWarehouse)
admin.site.register(TeaserMaker)
admin.site.register(ResellerNetwork)
admin.site.register(AdvertiseContent)
admin.site.register(ForwardToPortal)
admin.site.register(CommunicationChannel)
admin.site.register(Registrar)
