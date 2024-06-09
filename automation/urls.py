from django.urls import path

from automation.views import CreditCardView, CustomerView, RequestedProductProcessingView, \
    ProductRelationView, ProductWarehouseView

app_name = 'automation'

urlpatterns = [
    # Product Relation
    path('product-relation/list/', ProductRelationView().list, name='product-relation-list'),
    path('product-relation/filter/', ProductRelationView().filter, name='product-relation-filter'),
    path('product-relation/create/', ProductRelationView().create, name='product-relation-create'),
    path('product-relation/detail/', ProductRelationView().detail, name='product-relation-detail'),
    path('product-relation/modify/', ProductRelationView().modify, name='product-relation-modify'),
    path('product-relation/delete&id=<int:product_relation_id>/', ProductRelationView().delete, name='product-relation-delete-with-id'),

    # Product
    path('product-warehouse/list/', ProductWarehouseView().list, name='product-warehouse-list'),
    path('product-warehouse/filter/', ProductWarehouseView().filter, name='product-warehouse-filter'),
    path('product-warehouse/detail/', ProductWarehouseView().detail, name='product-warehouse-detail'),
    path('product-warehouse/modify/', ProductWarehouseView().modify, name='product-warehouse-modify'),

    # Credit Card
    path('credit-card/list/', CreditCardView().list, name='credit-card-list'),
    path('credit-card/filter/', CreditCardView().filter, name='credit-card-filter'),
    path('credit-card/create/', CreditCardView().create, name='credit-card-create'),
    path('credit-card/detail/', CreditCardView().detail, name='credit-card-detail'),
    path('credit-card/modify/', CreditCardView().modify, name='credit-card-modify'),
    path('credit-card/delete&id=<int:credit_card_id>/', CreditCardView().delete, name='credit-card-delete-with-id'),
    path('credit-card/change-state&id=<int:credit_card_id>/', CreditCardView().change_state,
         name='credit-card-change_state-with-id'),

    # Customer
    path('customer/list/', CustomerView().list, name='customer-list'),
    path('customer/filter/', CustomerView().filter, name='customer-filter'),
    path('customer/detail/', CustomerView().detail, name='customer-detail'),
    path('customer/modify/', CustomerView().modify, name='customer-modify'),
    path('customer/delete&id=<int:customer_id>/', CustomerView().delete, name='customer-delete-with-id'),

    # Requested Product Processing
    path('requested-product-processing/admin-list/', RequestedProductProcessingView().admin_list,
         name='requested-product-processing-admin-list'),
    path('requested-product-processing/public-list/', RequestedProductProcessingView().public_list,
         name='requested-product-processing-public-list'),
    path('requested-product-processing/list/', RequestedProductProcessingView().list,
         name='requested-product-processing-list'),
    path('requested-product-processing/filter/', RequestedProductProcessingView().filter,
         name='requested-product-processing-filter'),
    path('requested-product-processing/change-sale-state/', RequestedProductProcessingView().change_sale_state,
         name='requested-product-processing-change-sale-state'),


    path('requested-product-processing/assign-myself/', RequestedProductProcessingView().assign_myself,
         name='requested-product-processing-assign-myself'),


    path('requested-product-processing/change-warehouse-state/',
         RequestedProductProcessingView().change_warehouse_state,
         name='requested-product-processing-change-warehouse-state'),
    path('requested-product-processing/change-delivery-state/', RequestedProductProcessingView().change_delivery_state,
         name='requested-product-processing-change-delivery-state'),
    path('requested-product-processing/confirm-sale/', RequestedProductProcessingView().confirm_sale,
         name='requested-product-processing-confirm-sale'),
    path('requested-product-processing/reopen-sale/', RequestedProductProcessingView().reopen_sale,
         name='requested-product-processing-reopen-sale'),
    path('requested-product-processing/overall-data/', RequestedProductProcessingView().overall_data,
         name='requested-product-processing-overall-data'),
    path('requested-product-processing/product-detail/', RequestedProductProcessingView().product_detail,
         name='requested-product-processing-product-detail'),
    path('requested-product-processing/customer-detail/', RequestedProductProcessingView().customer_detail,
         name='requested-product-processing-customer-detail'),
    path('requested-product-processing/modify-customer-data/', RequestedProductProcessingView().modify_customer_data,
         name='requested-product-processing-modify-customer-data'),
    path('requested-product-processing/reports/', RequestedProductProcessingView().reports,
         name='requested-product-processing-reports'),
]
