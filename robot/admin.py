from django.contrib import admin

from robot.models import RequestedProductThreadIsActive, ProductWarehouseThreadIsActive


@admin.register(RequestedProductThreadIsActive)
class RequestedProductThreadIsActiveAdmin(admin.ModelAdmin):
    list_display = (
        'updated_at_display',
    )

    readonly_fields = (
        'updated_at',
    )

    fields = (
        'updated_at',
    )

    def has_add_permission(self, request):
        if RequestedProductThreadIsActive.objects.all().count() == 0:
            return True
        else:
            return False

    @admin.display(description="تاریخ بروزرسانی", empty_value='???')
    def updated_at_display(self, obj):
        data_time = str(obj.updated_at.strftime('%Y-%m-%d - %H:%M'))
        return data_time


@admin.register(ProductWarehouseThreadIsActive)
class ProductWarehouseThreadIsActiveAdmin(admin.ModelAdmin):
    list_display = (
        'updated_at_display',
    )

    readonly_fields = (
        'updated_at',
    )

    fields = (
        'updated_at',
    )

    def has_add_permission(self, request):
        if ProductWarehouseThreadIsActive.objects.all().count() == 0:
            return True
        else:
            return False

    @admin.display(description="تاریخ بروزرسانی", empty_value='???')
    def updated_at_display(self, obj):
        data_time = str(obj.updated_at.strftime('%Y-%m-%d - %H:%M'))
        return data_time