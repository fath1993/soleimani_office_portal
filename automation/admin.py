from django.contrib import admin

from automation.models import CreditCard, RequestedProductProcessing, Customer, RequestedProduct, \
    RequestedProductProcessingReport, ProductRelation


@admin.register(ProductRelation)
class ProductRelationAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'receiver',
        'number',
    )

    readonly_fields = (
        'created_at',
        'created_by',
    )

    fields = (
        'product',
        'receiver',
        'number',
        'created_at',
        'created_by',
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


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'phone_number',
        'full_name',
        'age',
        'address',
    )

    readonly_fields = (
        'created_at',
    )

    fields = (
        'phone_number',
        'full_name',
        'age',
        'address',
        'desired_product',
        'created_at',
    )


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = (
        'bank_name',
        'account_number',
        'card_number',
        'isbn',
        'owner',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    fields = (
        'bank_name',
        'account_number',
        'card_number',
        'isbn',
        'owner',
        'broker',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
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


@admin.register(RequestedProduct)
class RequestedProductAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'customer',
        'is_product_available_at_warehouse',
        'is_processed',
        'created_at_display',
        'updated_at_display',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fields = (
        'product',
        'customer',
        'is_product_available_at_warehouse',
        'is_processed',
        'created_at',
        'updated_at',
    )

    @admin.display(description="تاریخ ایجاد", empty_value='???')
    def created_at_display(self, obj):
        data_time = str(obj.created_at.strftime('%Y-%m-%d - %H:%M'))
        return data_time

    @admin.display(description="تاریخ بروزرسانی", empty_value='???')
    def updated_at_display(self, obj):
        data_time = str(obj.updated_at.strftime('%Y-%m-%d - %H:%M'))
        return data_time


@admin.register(RequestedProductProcessing)
class RequestedProductProcessingAdmin(admin.ModelAdmin):
    list_display = (
        'requested_product',
        'in_department_status',
        'sales_status',
        'warehouse_status',
        'delivery_status',
        'updated_at_display',
    )

    readonly_fields = (
        'requested_product',
        'seller',
        'warehouse_keeper',
        'delivery_man',
        'created_at',
        'updated_at',
        'updated_by',
    )

    fields = (
        'requested_product',
        'in_department_status',
        'seller',
        'is_confirmed_by_sales_department',
        'sales_status',
        'product_price',
        'product_number',
        'request_total_income',
        'warehouse_keeper',
        'warehouse_status',
        'is_confirmed_by_warehouse_keeper',
        'is_confirmed_by_warehouse_department',
        'delivery_man',
        'delivery_status',
        'is_confirmed_by_delivery_man',
        'is_confirmed_by_delivery_department',
        'created_at',
        'updated_at',
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


@admin.register(RequestedProductProcessingReport)
class RequestedProductProcessingReportAdmin(admin.ModelAdmin):
    list_display = (
        'requested_product_processing',
        'department',
        'report',
    )

    readonly_fields = (
        'requested_product_processing',
        'department',
        'created_at',
        'created_by',
    )

    fields = (
        'requested_product_processing',
        'department',
        'report',
        'created_at',
        'created_by',
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
