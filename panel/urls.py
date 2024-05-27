from django.urls import path

from panel.views import DashboardView, PermissionView, RoleView, ProductView, TeaserMakerView, \
    ResellerNetworkView, ReceiverView, AdvertiseContentView, ForwardToPortalView, CommunicationChannelView, \
    RegistrarView
from panel.viewsAutomation import CreditCardView, CustomerView, RequestedProductView, RequestedProductProcessingView

app_name = 'panel'

urlpatterns = [
    path('', DashboardView().main, name='panel-dashboard'),

    # Permission
    path('permission/list/', PermissionView().list, name='permission-list'),
    path('permission/filter/', PermissionView().filter, name='permission-filter'),
    path('permission/create/', PermissionView().create, name='permission-create'),
    path('permission/detail&id=<int:permission_id>/', PermissionView().detail, name='permission-detail-with-id'),
    path('permission/modify&id=<int:permission_id>/', PermissionView().modify, name='permission-modify-with-id'),
    path('permission/delete&id=<int:permission_id>/', PermissionView().delete, name='permission-delete-with-id'),

    # Role
    path('role/list/', RoleView().list, name='role-list'),
    path('role/filter/', RoleView().filter, name='role-filter'),
    path('role/create/', RoleView().create, name='role-create'),
    path('role/detail&id=<int:role_id>/', RoleView().detail, name='role-detail-with-id'),
    path('role/modify&id=<int:role_id>/', RoleView().modify, name='role-modify-with-id'),
    path('role/delete&id=<int:role_id>/', RoleView().delete, name='role-delete-with-id'),

    # Product
    path('product/list/', ProductView().list, name='product-list'),
    path('product/filter/', ProductView().filter, name='product-filter'),
    path('product/create/', ProductView().create, name='product-create'),
    path('product/detail&id=<int:product_id>/', ProductView().detail, name='product-detail-with-id'),
    path('product/modify&id=<int:product_id>/', ProductView().modify, name='product-modify-with-id'),
    path('product/delete&id=<int:product_id>/', ProductView().delete, name='product-delete-with-id'),
    path('product/delete-file&file-id=<int:file_id>/', ProductView().delete_file, name='product-delete-file-with-file-id'),
    path('product/change-state&id=<int:product_id>/', ProductView().change_state, name='product-change_state-with-id'),

    # Teaser Maker
    path('teaser-maker/list/', TeaserMakerView().list, name='teaser-maker-list'),
    path('teaser-maker/filter/', TeaserMakerView().filter, name='teaser-maker-filter'),
    path('teaser-maker/create/', TeaserMakerView().create, name='teaser-maker-create'),
    path('teaser-maker/detail&id=<int:teaser_maker_id>/', TeaserMakerView().detail, name='teaser-maker-detail-with-id'),
    path('teaser-maker/modify&id=<int:teaser_maker_id>/', TeaserMakerView().modify, name='teaser-maker-modify-with-id'),
    path('teaser-maker/delete&id=<int:teaser_maker_id>/', TeaserMakerView().delete, name='teaser-maker-delete-with-id'),
    path('teaser-maker/change-state&id=<int:teaser_maker_id>/', TeaserMakerView().change_state, name='teaser-maker-change_state-with-id'),

    # Reseller Network
    path('reseller-network/list/', ResellerNetworkView().list, name='reseller-network-list'),
    path('reseller-network/filter/', ResellerNetworkView().filter, name='reseller-network-filter'),
    path('reseller-network/create/', ResellerNetworkView().create, name='reseller-network-create'),
    path('reseller-network/detail&id=<int:reseller_network_id>/', ResellerNetworkView().detail, name='reseller-network-detail-with-id'),
    path('reseller-network/modify&id=<int:reseller_network_id>/', ResellerNetworkView().modify, name='reseller-network-modify-with-id'),
    path('reseller-network/delete&id=<int:reseller_network_id>/', ResellerNetworkView().delete, name='reseller-network-delete-with-id'),

    # Receiver
    path('receiver/list/', ReceiverView().list, name='receiver-list'),
    path('receiver/filter/', ReceiverView().filter, name='receiver-filter'),
    path('receiver/create/', ReceiverView().create, name='receiver-create'),
    path('receiver/detail&id=<int:receiver_id>/', ReceiverView().detail, name='receiver-detail-with-id'),
    path('receiver/modify&id=<int:receiver_id>/', ReceiverView().modify, name='receiver-modify-with-id'),
    path('receiver/delete&id=<int:receiver_id>/', ReceiverView().delete, name='receiver-delete-with-id'),

    # Advertise Content
    path('advertise-content/list/', AdvertiseContentView().list, name='advertise-content-list'),
    path('advertise-content/filter/', AdvertiseContentView().filter, name='advertise-content-filter'),
    path('advertise-content/create/', AdvertiseContentView().create, name='advertise-content-create'),
    path('advertise-content/detail&id=<int:advertise_content_id>/', AdvertiseContentView().detail, name='advertise-content-detail-with-id'),
    path('advertise-content/modify&id=<int:advertise_content_id>/', AdvertiseContentView().modify, name='advertise-content-modify-with-id'),
    path('advertise-content/delete&id=<int:advertise_content_id>/', AdvertiseContentView().delete, name='advertise-content-delete-with-id'),

    # Forward To Portal
    path('forward-to-portal/list/', ForwardToPortalView().list, name='forward-to-portal-list'),
    path('forward-to-portal/filter/', ForwardToPortalView().filter, name='forward-to-portal-filter'),
    path('forward-to-portal/create/', ForwardToPortalView().create, name='forward-to-portal-create'),
    path('forward-to-portal/detail&id=<int:forward_to_portal_id>/', ForwardToPortalView().detail, name='forward-to-portal-detail-with-id'),
    path('forward-to-portal/modify&id=<int:forward_to_portal_id>/', ForwardToPortalView().modify, name='forward-to-portal-modify-with-id'),
    path('forward-to-portal/delete&id=<int:forward_to_portal_id>/', ForwardToPortalView().delete, name='forward-to-portal-delete-with-id'),

    # Communication Channel
    path('communication-channel/list/', CommunicationChannelView().list, name='communication-channel-list'),
    path('communication-channel/filter/', CommunicationChannelView().filter, name='communication-channel-filter'),
    path('communication-channel/create/', CommunicationChannelView().create, name='communication-channel-create'),
    path('communication-channel/detail&id=<int:communication_channel_id>/', CommunicationChannelView().detail, name='communication-channel-detail-with-id'),
    path('communication-channel/modify&id=<int:communication_channel_id>/', CommunicationChannelView().modify, name='communication-channel-modify-with-id'),
    path('communication-channel/delete&id=<int:communication_channel_id>/', CommunicationChannelView().delete, name='communication-channel-delete-with-id'),

    # Registrar
    path('registrar/list/', RegistrarView().list, name='registrar-list'),
    path('registrar/filter/', RegistrarView().filter, name='registrar-filter'),
    path('registrar/create/', RegistrarView().create, name='registrar-create'),
    path('registrar/detail&id=<int:registrar_id>/', RegistrarView().detail, name='registrar-detail-with-id'),
    path('registrar/modify&id=<int:registrar_id>/', RegistrarView().modify, name='registrar-modify-with-id'),
    path('registrar/delete&id=<int:registrar_id>/', RegistrarView().delete, name='registrar-delete-with-id'),

    # Credit Card
    path('credit-card/list/', CreditCardView().list, name='credit-card-list'),
    path('credit-card/filter/', CreditCardView().filter, name='credit-card-filter'),
    path('credit-card/create/', CreditCardView().create, name='credit-card-create'),
    path('credit-card/detail&id=<int:credit_card_id>/', CreditCardView().detail, name='credit-card-detail-with-id'),
    path('credit-card/modify&id=<int:credit_card_id>/', CreditCardView().modify, name='credit-card-modify-with-id'),
    path('credit-card/delete&id=<int:credit_card_id>/', CreditCardView().delete, name='credit-card-delete-with-id'),
    path('credit-card/change-state&id=<int:credit_card_id>/', CreditCardView().change_state, name='credit-card-change_state-with-id'),

    # Customer
    path('customer/list/', CustomerView().list, name='customer-list'),
    path('customer/filter/', CustomerView().filter, name='customer-filter'),
    path('customer/create/', CustomerView().create, name='customer-create'),
    path('customer/detail&id=<int:customer_id>/', CustomerView().detail, name='customer-detail-with-id'),
    path('customer/modify&id=<int:customer_id>/', CustomerView().modify, name='customer-modify-with-id'),
    path('customer/delete&id=<int:customer_id>/', CustomerView().delete, name='customer-delete-with-id'),
    path('customer/change-state&id=<int:customer_id>/', CustomerView().change_state, name='customer-change_state-with-id'),

    # Requested Product
    path('requested-product/list/', RequestedProductView().list, name='requested-product-list'),
    path('requested-product/filter/', RequestedProductView().filter, name='requested-product-filter'),
    path('requested-product/create/', RequestedProductView().create, name='requested-product-create'),
    path('requested-product/detail&id=<int:requested_product_id>/', RequestedProductView().detail, name='requested-product-detail-with-id'),
    path('requested-product/modify&id=<int:requested_product_id>/', RequestedProductView().modify, name='requested-product-modify-with-id'),
    path('requested-product/delete&id=<int:requested_product_id>/', RequestedProductView().delete, name='requested-product-delete-with-id'),
    path('requested-product/change-state&id=<int:requested_product_id>/', RequestedProductView().change_state, name='requested-product-change_state-with-id'),

    # Requested Product Processing
    path('requested-product-processing/admin-list/', RequestedProductProcessingView().admin_list,
         name='requested-product-processing-admin-list'),
    path('requested-product-processing/public-list/', RequestedProductProcessingView().public_list, name='requested-product-processing-public-list'),
    path('requested-product-processing/list/', RequestedProductProcessingView().list, name='requested-product-processing-list'),
    path('requested-product-processing/filter/', RequestedProductProcessingView().filter, name='requested-product-processing-filter'),
    path('requested-product-processing/change-sale-state/', RequestedProductProcessingView().change_sale_state, name='requested-product-processing-change-sale-state'),
    path('requested-product-processing/change-warehouse-state/', RequestedProductProcessingView().change_warehouse_state,
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
    path('requested-product-processing/reports/', RequestedProductProcessingView().reports,
         name='requested-product-processing-reports'),
]
