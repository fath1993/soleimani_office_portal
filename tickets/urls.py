from django.urls import path

from tickets.views import TicketView, MessageView, NotificationView

app_name = 'ticket'

urlpatterns = [
    # Ticket
    path('list&box-status=<str:box_status>/', TicketView().list, name='ticket-list-with-box-status'),
    path('filter/', TicketView().filter, name='ticket-filter'),
    path('ticket-create/', TicketView().create, name='ticket-create'),
    path('detail&id=<int:ticket_id>/', TicketView().detail, name='ticket-detail-with-id'),
    path('delete&id=<int:ticket_id>/', TicketView().delete, name='ticket-delete-with-id'),
    path('change-state&id=<int:ticket_id>/', TicketView().change_state, name='ticket-change_state-with-id'),

    # Message
    path('message/list/', MessageView().list, name='message-list'),
    path('message/create&id=<int:ticket_id>/', MessageView().create, name='message-create'),
    path('message/detail&id=<int:ticket_id>/', MessageView().detail, name='message-detail-with-id'),

    # Notification
    path('notification/list/', NotificationView().list, name='notification-list'),
    path('notification/filter/', NotificationView().filter, name='notification-filter'),
    path('notification/notification-create/', NotificationView().create, name='notification-create'),
    path('notification/detail&id=<int:notification_id>/', NotificationView().detail, name='notification-detail-with-id'),
    path('notification/change-state&id=<int:notification_id>/', NotificationView().change_state, name='notification-change_state-with-id'),

]

