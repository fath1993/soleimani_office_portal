from django.urls import path

from resource.views import ProductView, TeaserMakerView, ResellerNetworkView, ReceiverView, AdvertiseContentView, ForwardToPortalView, CommunicationChannelView, RegistrarView

app_name = 'resource'

urlpatterns = [
    # Product
    path('product/list/', ProductView().list, name='product-list'),
    path('product/filter/', ProductView().filter, name='product-filter'),
    path('product/create/', ProductView().create, name='product-create'),
    path('product/detail/', ProductView().detail, name='product-detail'),
    path('product/modify/', ProductView().modify, name='product-modify'),
    path('product/delete&id=<int:product_id>/', ProductView().delete, name='product-delete-with-id'),
    path('product/change-state/', ProductView().change_state, name='product-change-state'),

    # Teaser Maker
    path('teaser-maker/list/', TeaserMakerView().list, name='teaser-maker-list'),
    path('teaser-maker/filter/', TeaserMakerView().filter, name='teaser-maker-filter'),
    path('teaser-maker/create/', TeaserMakerView().create, name='teaser-maker-create'),
    path('teaser-maker/detail/', TeaserMakerView().detail, name='teaser-maker-detail'),
    path('teaser-maker/modify/', TeaserMakerView().modify, name='teaser-maker-modify'),
    path('teaser-maker/delete&id=<int:teaser_maker_id>/', TeaserMakerView().delete, name='teaser-maker-delete-with-id'),
    path('teaser-maker/change-state/', TeaserMakerView().change_state, name='teaser-maker-change-state'),

    # Reseller Network
    path('reseller-network/list/', ResellerNetworkView().list, name='reseller-network-list'),
    path('reseller-network/filter/', ResellerNetworkView().filter, name='reseller-network-filter'),
    path('reseller-network/create/', ResellerNetworkView().create, name='reseller-network-create'),
    path('reseller-network/detail/', ResellerNetworkView().detail, name='reseller-network-detail'),
    path('reseller-network/modify/', ResellerNetworkView().modify, name='reseller-network-modify'),
    path('reseller-network/delete&id=<int:reseller_network_id>/', ResellerNetworkView().delete, name='reseller-network-delete-with-id'),
    path('reseller-network/change-state/', ResellerNetworkView().change_state, name='reseller-network-change-state'),

    # Receiver
    path('receiver/list/', ReceiverView().list, name='receiver-list'),
    path('receiver/filter/', ReceiverView().filter, name='receiver-filter'),
    path('receiver/create/', ReceiverView().create, name='receiver-create'),
    path('receiver/detail/', ReceiverView().detail, name='receiver-detail'),
    path('receiver/modify/', ReceiverView().modify, name='receiver-modify'),
    path('receiver/delete&id=<int:receiver_id>/', ReceiverView().delete, name='receiver-delete-with-id'),
    path('receiver/change-state/', ReceiverView().change_state, name='receiver-change-state'),

    # Advertise Content
    path('advertise-content/list/', AdvertiseContentView().list, name='advertise-content-list'),
    path('advertise-content/filter/', AdvertiseContentView().filter, name='advertise-content-filter'),
    path('advertise-content/create/', AdvertiseContentView().create, name='advertise-content-create'),
    path('advertise-content/detail/', AdvertiseContentView().detail, name='advertise-content-detail'),
    path('advertise-content/modify/', AdvertiseContentView().modify, name='advertise-content-modify'),
    path('advertise-content/delete&id=<int:advertise_content_id>/', AdvertiseContentView().delete, name='advertise-content-delete-with-id'),
    path('advertise-content/change-state/', AdvertiseContentView().change_state, name='advertise-content-change-state'),

    # Forward To Portal
    path('forward-to-portal/list/', ForwardToPortalView().list, name='forward-to-portal-list'),
    path('forward-to-portal/filter/', ForwardToPortalView().filter, name='forward-to-portal-filter'),
    path('forward-to-portal/create/', ForwardToPortalView().create, name='forward-to-portal-create'),
    path('forward-to-portal/detail/', ForwardToPortalView().detail, name='forward-to-portal-detail'),
    path('forward-to-portal/modify/', ForwardToPortalView().modify, name='forward-to-portal-modify'),
    path('forward-to-portal/delete&id=<int:forward_to_portal_id>/', ForwardToPortalView().delete, name='forward-to-portal-delete-with-id'),
    path('forward-to-portal/change-state/', ForwardToPortalView().change_state, name='forward-to-portal-change-state'),

    # Communication Channel
    path('communication-channel/list/', CommunicationChannelView().list, name='communication-channel-list'),
    path('communication-channel/filter/', CommunicationChannelView().filter, name='communication-channel-filter'),
    path('communication-channel/create/', CommunicationChannelView().create, name='communication-channel-create'),
    path('communication-channel/detail/', CommunicationChannelView().detail, name='communication-channel-detail'),
    path('communication-channel/modify/', CommunicationChannelView().modify, name='communication-channel-modify'),
    path('communication-channel/delete&id=<int:communication_channel_id>/', CommunicationChannelView().delete, name='communication-channel-delete-with-id'),
    path('communication-channel/change-state/', CommunicationChannelView().change_state, name='communication-channel-change-state'),

    # Registrar
    path('registrar/list/', RegistrarView().list, name='registrar-list'),
    path('registrar/filter/', RegistrarView().filter, name='registrar-filter'),
    path('registrar/create/', RegistrarView().create, name='registrar-create'),
    path('registrar/detail/', RegistrarView().detail, name='registrar-detail'),
    path('registrar/modify/', RegistrarView().modify, name='registrar-modify'),
    path('registrar/delete&id=<int:registrar_id>/', RegistrarView().delete, name='registrar-delete-with-id'),
    path('registrar/change-state/', RegistrarView().change_state, name='registrar-change-state'),

]
