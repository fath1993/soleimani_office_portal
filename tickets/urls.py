from django.urls import path

from tickets.views import TicketView, TicketAdminView, MessageView

app_name = 'ticket'

urlpatterns = [
    # Ticket
    path('list/', TicketView().list, name='ticket-list'),
    path('filter/', TicketView().filter, name='ticket-filter'),
    path('create/', TicketView().create, name='ticket-create'),
    path('detail&id=<int:ticket_id>/', TicketView().detail, name='ticket-detail-with-id'),
    path('close&id=<int:ticket_id>/', TicketView().close, name='ticket-close-with-id'),

    # Ticket Admin
    path('admin-list/', TicketAdminView().list, name='ticket-admin-list'),
    path('admin-filter/', TicketAdminView().filter, name='ticket-admin-filter'),
    path('admin-create/', TicketAdminView().create, name='ticket-admin-create'),
    path('admin-detail&id=<int:ticket_id>/', TicketAdminView().detail, name='ticket-admin-detail-with-id'),
    path('admin-modify&id=<int:ticket_id>/', TicketAdminView().modify, name='ticket-admin-modify-with-id'),
    path('admin-delete&id=<int:ticket_id>/', TicketAdminView().delete, name='ticket-admin-delete-with-id'),
    path('admin-close&id=<int:ticket_id>/', TicketAdminView().close, name='ticket-admin-close-with-id'),

    # Message
    path('message/list/', MessageView().list, name='message-list'),
    path('message/create&id=<int:ticket_id>/', MessageView().create, name='message-create'),
    path('message/detail&id=<int:ticket_id>/', MessageView().detail, name='message-detail-with-id'),
]

