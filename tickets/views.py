import threading

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect

from accounts.models import UserNotification
from accounts.templatetags.account_custom_tag import has_access_to_section
from gallery.models import FileGallery
from accounts.custom_decorator import RequireMethod
from panel.views import CheckLogin, CheckPermissions
from portal.models import TeaserMaker

from tickets.models import Ticket, Message, Notification
from tickets.serializer import MessageSerializer
from utilities.http_metod import fetch_data_from_http_post, \
    fetch_files_from_http_post_data, fetch_data_from_http_get


class TicketView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='read')
    def list(self, request, box_status, *args, **kwargs):
        q = Q()
        if box_status == 'sent':
            q &= (
                Q(**{'owner': request.user})
            )
            context = {'page_title': 'صندوق پیام های ارسالی', 'get_params': request.GET.urlencode()}
        elif box_status == 'received':
            q &= (
                Q(**{'receiver': request.user})
            )
            context = {'page_title': 'صندوق پیام های دریافتی', 'get_params': request.GET.urlencode()}
        elif box_status == 'all':
            if not has_access_to_section(request.user, 'read,ticket_admin'):
                return render(request, 'panel/err/err-not-authorized.html')
            context = {'page_title': 'مدیریت پیام های کاربران سامانه', 'get_params': request.GET.urlencode()}
        else:
            return render(request, 'panel/err/err-not-found.html')

        tickets = Ticket.objects.filter(q).order_by('-created_at')
        context['tickets'] = tickets

        items_per_page = 50
        paginator = Paginator(tickets, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/tickets/ticket-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='read')
    def detail(self, request, ticket_id, *args, **kwargs):
        try:
            q = Q()
            q &= Q(
                Q(**{'id': ticket_id})
            )
            if not has_access_to_section(request, 'read,create,modify,delete,ticket_admin'):
                q &= Q(
                    Q(**{'owner': request.user}) |
                    Q(**{'receiver': request.user})
                )
            ticket = Ticket.objects.get(q)

            z = Q()
            z &= Q(
                Q(**{'ticket__id': ticket_id})
            )
            if not has_access_to_section(request, 'read,create,modify,delete,ticket_admin'):
                z &= Q(
                    Q(**{'ticket__owner': request.user}) |
                    Q(**{'ticket__receiver': request.user})
                )

            messages = Message.objects.filter(z)
            context = {'page_title': f'جزئیات پیام با موضوع *{ticket.subject}*',
                       'ticket': ticket, 'messages': messages, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/tickets/ticket-detail.html', context)
        except Exception as e:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        context = {}
        search = fetch_data_from_http_get(request, 'search', context)
        content_type = fetch_data_from_http_get(request, 'content_type', context)
        is_active = fetch_data_from_http_get(request, 'is_active', context)
        address = fetch_data_from_http_get(request, 'address', context)
        phone_number = fetch_data_from_http_get(request, 'phone_number', context)
        creation_price_from = fetch_data_from_http_get(request, 'creation_price_from', context)
        creation_price_to = fetch_data_from_http_get(request, 'creation_price_to', context)
        editing_price_from = fetch_data_from_http_get(request, 'editing_price_from', context)
        editing_price_to = fetch_data_from_http_get(request, 'editing_price_to', context)

        page_title = f''''''
        q = Q()
        if search:
            page_title += f'search: {search}, '
            if search.isdigit():
                q &= (
                    Q(**{'id': search})
                )
            else:
                q &= (
                        Q(**{'name__icontains': search}) |
                        Q(**{'code': search})
                )

        if content_type:
            page_title += f'content_type: {content_type}, '
            q &= (
                Q(**{'content_type': content_type})
            )

        if is_active:
            page_title += f'is_active: {is_active}, '
            if is_active == 'فعال':
                is_active = True
            else:
                is_active = False
            q &= (
                Q(**{'is_active': is_active})
            )

        if address:
            page_title += f'address: {address}, '
            q &= (
                Q(**{'address__icontains': address})
            )

        if phone_number:
            page_title += f'phone_number: {phone_number}, '
            q &= (
                Q(**{'phone_number__icontains': phone_number})
            )

        if creation_price_from:
            page_title += f'creation_price_from: {creation_price_from}, '
            q &= (
                Q(**{'creation_price__gte': int(creation_price_from)})
            )

        if creation_price_to:
            page_title += f'creation_price_to: {creation_price_to}, '
            q &= (
                Q(**{'creation_price__lte': int(creation_price_to)})
            )

        if editing_price_from:
            page_title += f'editing_price_from: {editing_price_from}, '
            q &= (
                Q(**{'editing_price__gte': int(editing_price_from)})
            )

        if editing_price_to:
            page_title += f'editing_price_to: {editing_price_to}, '
            q &= (
                Q(**{'editing_price__lte': int(editing_price_to)})
            )

        context['page_title'] = f'لیست تیزر ساز ها شامل *{page_title}*'
        context['get_params'] = request.GET.urlencode()

        teaser_makers = TeaserMaker.objects.filter(q).order_by('id')
        context['teaser_makers'] = teaser_makers

        items_per_page = 50
        paginator = Paginator(teaser_makers, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/teaser-maker/teaser-maker-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='create')
    @RequireMethod(allowed_method='POST')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت پیام جدید', 'get_params': request.GET.urlencode()}

        subject = fetch_data_from_http_post(request, 'subject', context)
        receiver = fetch_data_from_http_post(request, 'receiver', context)
        content = fetch_data_from_http_post(request, 'content', context)
        files = fetch_files_from_http_post_data(request, 'files', context)

        if not subject:
            context['err'] = 'موضوع پیام بدرستی وارد نشده است'
            return render(request, 'panel/tickets/ticket-list.html', context)
        if not receiver:
            context['err'] = 'شناسه گیرنده بدرستی وارد نشده است'
            return render(request, 'panel/tickets/ticket-list.html', context)
        else:
            username = str(receiver).replace('#', '')
        if not content:
            context['err'] = 'محتوای پیام بدرستی وارد نشده است'
            return render(request, 'panel/tickets/ticket-list.html', context)

        try:
            receiver = User.objects.get(username=username)
        except:
            context['err'] = f'شناسه پیام رسانی گیرنده با مقدار {username} یافت نشد'
            return render(request, 'panel/tickets/ticket-list.html', context)

        new_ticket = Ticket.objects.create(
            status='created',
            subject=subject,
            owner=request.user,
            receiver=receiver,
            has_seen_by_owner=True,
            has_seen_by_receiver=False,
            created_by=request.user,
            updated_by=request.user,
        )

        new_message = Message.objects.create(
            ticket=new_ticket,
            content=content,
            created_by=request.user,
        )

        for file in files:
            try:
                new_file = FileGallery.objects.create(
                    alt=file.name,
                    file=file,
                    created_by=request.user,
                )
                new_message.attachments.add(new_file)
            except:
                pass

        context['message'] = f'پیام با شناسه یکتای {new_ticket.id} ایجاد گردید'
        return redirect(
            reverse('ticket:ticket-list-with-box-status',
                    kwargs={'box_status': 'sent'}) + f'?{request.GET.urlencode()}')

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='modify')
    def modify(self, request, teaser_maker_id, *args, **kwargs):
        try:
            teaser_maker = TeaserMaker.objects.get(id=teaser_maker_id)
            context = {'page_title': f'ویرایش اطلاعات تیزر ساز *{teaser_maker.name}*',
                       'teaser_maker': teaser_maker, 'get_params': request.GET.urlencode()}

            if request.method == 'GET':
                return render(request, 'panel/teaser-maker/teaser-maker-edit.html', context)
            else:
                name = fetch_data_from_http_post(request, 'name', context)
                content_type = fetch_data_from_http_post(request, 'content_type', context)
                code = fetch_data_from_http_post(request, 'code', context)
                address = fetch_data_from_http_post(request, 'address', context)
                phone_number = fetch_data_from_http_post(request, 'phone_number', context)
                creation_price = fetch_data_from_http_post(request, 'creation_price', context)
                editing_price = fetch_data_from_http_post(request, 'editing_price', context)
                is_active = fetch_data_from_http_post(request, 'is_active', context)

                try:
                    if name:
                        teaser_maker.name = name
                    if content_type:
                        teaser_maker.content_type = content_type
                    if code:
                        teaser_maker.code = code
                    if address:
                        teaser_maker.address = address
                    if phone_number:
                        teaser_maker.phone_number = phone_number
                    if creation_price:
                        teaser_maker.creation_price = creation_price
                    if editing_price:
                        teaser_maker.editing_price = editing_price
                    if is_active == 'true':
                        is_active = True
                    else:
                        is_active = False
                    teaser_maker.is_active = is_active
                    teaser_maker.save()
                    context['message'] = f'تیزر ساز با شناسه یکتا {teaser_maker.id} ویرایش گردید'
                    return redirect(
                        reverse('panel:teaser-maker-detail-with-id',
                                kwargs={'teaser_maker_id': teaser_maker_id}) + f'?{request.GET.urlencode()}')
                except:
                    return render(request, 'panel/err/err-not-found.html')
        except Exception as e:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='delete')
    def delete(self, request, teaser_maker_id, *args, **kwargs):
        try:
            teaser_maker = TeaserMaker.objects.get(id=teaser_maker_id)
            context = {'page_title': f'حذف تیزر ساز {teaser_maker.name}', 'get_params': request.GET.urlencode()}
            teaser_maker.delete()
            return redirect(reverse('panel:teaser-maker-list') + f'?{request.GET.urlencode()}')
        except Exception as e:
            print(e)
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='modify')
    def change_state(self, request, teaser_maker_id, *args, **kwargs):
        try:
            teaser_maker = TeaserMaker.objects.get(id=teaser_maker_id)
            context = {'page_title': f'تغییر وضعیت تیزر ساز {teaser_maker.name}', 'get_params': request.GET.urlencode()}
            if teaser_maker.is_active:
                teaser_maker.is_active = False
                teaser_maker_is_active = 'false'
            else:
                teaser_maker.is_active = True
                teaser_maker_is_active = 'true'
            teaser_maker.save()
            return JsonResponse({"teaser_maker_is_active": teaser_maker_is_active})
        except:
            return render(request, 'panel/err/err-not-found.html')


class NotificationView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'اطلاعیه ها', 'get_params': request.GET.urlencode()}
        q = Q()
        if not has_access_to_section(request, 'create,notification'):
            q &= (
                Q(**{'user': request.user})
            )
        notifications = UserNotification.objects.filter(q).order_by('-created_at')
        context['notifications'] = notifications

        items_per_page = 50
        paginator = Paginator(notifications, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/notifications/notification-list.html', context)

    @CheckLogin()
    def detail(self, request, notification_id, *args, **kwargs):
        try:
            user_notification = UserNotification.objects.get(id=notification_id)
            if user_notification.user != request.user:
                if not has_access_to_section(request, 'create,notification'):
                    return render(request, 'panel/err/err-not-authorized.html')
            context = {'page_title': f'جزئیات اطلاعیه با شماره *{user_notification.notification.id}*',
                       'user_notification': user_notification, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/notifications/notification-detail.html', context)
        except Exception as e:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='notification', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        context = {}
        search = fetch_data_from_http_get(request, 'search', context)
        content_type = fetch_data_from_http_get(request, 'content_type', context)
        is_active = fetch_data_from_http_get(request, 'is_active', context)
        address = fetch_data_from_http_get(request, 'address', context)
        phone_number = fetch_data_from_http_get(request, 'phone_number', context)
        creation_price_from = fetch_data_from_http_get(request, 'creation_price_from', context)
        creation_price_to = fetch_data_from_http_get(request, 'creation_price_to', context)
        editing_price_from = fetch_data_from_http_get(request, 'editing_price_from', context)
        editing_price_to = fetch_data_from_http_get(request, 'editing_price_to', context)

        page_title = f''''''
        q = Q()
        if search:
            page_title += f'search: {search}, '
            if search.isdigit():
                q &= (
                    Q(**{'id': search})
                )
            else:
                q &= (
                        Q(**{'name__icontains': search}) |
                        Q(**{'code': search})
                )

        if content_type:
            page_title += f'content_type: {content_type}, '
            q &= (
                Q(**{'content_type': content_type})
            )

        if is_active:
            page_title += f'is_active: {is_active}, '
            if is_active == 'فعال':
                is_active = True
            else:
                is_active = False
            q &= (
                Q(**{'is_active': is_active})
            )

        if address:
            page_title += f'address: {address}, '
            q &= (
                Q(**{'address__icontains': address})
            )

        if phone_number:
            page_title += f'phone_number: {phone_number}, '
            q &= (
                Q(**{'phone_number__icontains': phone_number})
            )

        if creation_price_from:
            page_title += f'creation_price_from: {creation_price_from}, '
            q &= (
                Q(**{'creation_price__gte': int(creation_price_from)})
            )

        if creation_price_to:
            page_title += f'creation_price_to: {creation_price_to}, '
            q &= (
                Q(**{'creation_price__lte': int(creation_price_to)})
            )

        if editing_price_from:
            page_title += f'editing_price_from: {editing_price_from}, '
            q &= (
                Q(**{'editing_price__gte': int(editing_price_from)})
            )

        if editing_price_to:
            page_title += f'editing_price_to: {editing_price_to}, '
            q &= (
                Q(**{'editing_price__lte': int(editing_price_to)})
            )

        context['page_title'] = f'لیست تیزر ساز ها شامل *{page_title}*'
        context['get_params'] = request.GET.urlencode()

        teaser_makers = TeaserMaker.objects.filter(q).order_by('id')
        context['teaser_makers'] = teaser_makers

        items_per_page = 50
        paginator = Paginator(teaser_makers, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/teaser-maker/teaser-maker-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='notification', allowed_actions='create')
    @RequireMethod(allowed_method='POST')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت اطلاعیه جدید', 'get_params': request.GET.urlencode()}

        content = fetch_data_from_http_post(request, 'content', context)
        files = fetch_files_from_http_post_data(request, 'files', context)

        if not content:
            context['err'] = 'پیام اطلاعیه بدرستی وارد نشده است'
            return render(request, 'panel/notifications/notification-list.html', context)

        new_notification = Notification.objects.create(
            content=content,
            created_by=request.user,
        )

        for file in files:
            try:
                new_file = FileGallery.objects.create(
                    alt=file.name,
                    file=file,
                    created_by=request.user,
                )
                new_notification.attachments.add(new_file)
            except:
                pass
        SendNotificationThread(notification=new_notification).start()

        context['message'] = f'اطلاعیه با شماره {new_notification.id} ایجاد گردید'
        return redirect('ticket:notification-list')

    @CheckLogin()
    def change_state(self, request, notification_id, *args, **kwargs):
        try:
            notification = UserNotification.objects.get(id=notification_id)
            if notification.user != request.user:
                return JsonResponse({"notification_has_seen_by_user": 'false'})
            if not notification.has_seen_by_user:
                notification.has_seen_by_user = True
                notification_has_seen_by_user = 'true'
                notification.save()
            else:
                notification_has_seen_by_user = 'false'
            return JsonResponse({"notification_has_seen_by_user": notification_has_seen_by_user})
        except:
            return render(request, 'panel/err/err-not-found.html')


class SendNotificationThread(threading.Thread):
    def __init__(self, notification):
        super().__init__()
        self.notification = notification

    def run(self):
        for user in User.objects.all():
            try:
                UserNotification.objects.create(
                    user=user,
                    notification=self.notification,
                )
            except:
                pass


class MessageView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='message', allowed_actions='read')
    def list(self, request, ticket_id, *args, **kwargs):
        q = Q()
        q &= Q(
            Q(**{'ticket__id': ticket_id})
        )
        if not has_access_to_section(request, 'read,create,modify,delete,ticket_admin'):
            q &= Q(
                Q(**{'ticket__owner': request.user}) |
                Q(**{'ticket__receiver': request.user})
            )

        messages = Message.objects.filter(q)

        serializer = MessageSerializer(messages, many=True)
        json_response_body = {
            "method": "post",
            "request": f"لیست پیام های تیکت با ایدی {ticket_id}",
            "result": "موفق",
            "data": serializer.data
        }
        return JsonResponse(json_response_body)

    @CheckLogin()
    def detail(self, request, message_id, *args, **kwargs):
        try:
            message = Message.objects.filter(id=message_id)
            if message.count() == 0:
                return render(request, 'panel/err/err-not-found.html')
            if not has_access_to_section(request, 'read,ticket_admin'):
                if message.ticket.belong_to != request.user:
                    return render(request, 'panel/err/err-not-authorized.html')
            serializer = MessageSerializer(message, many=True)

            json_response_body = {
                "method": "post",
                "request": f"محتوای پیام با ایدی {message_id}",
                "result": "موفق",
                "data": serializer.data
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    def create(self, request, ticket_id, *args, **kwargs):
        try:
            q = Q()
            q &= Q(
                Q(**{'id': ticket_id})
            )
            if not has_access_to_section(request, 'read,create,modify,delete,ticket_admin'):
                q &= Q(
                    Q(**{'owner': request.user}) |
                    Q(**{'receiver': request.user})
                )
            ticket = Ticket.objects.get(q)

            context = {'page_title': f'ساخت پیام جدید ذیل تیکت {ticket_id}', 'get_params': request.GET.urlencode()}

            content = fetch_data_from_http_post(request, 'content', context)
            files = fetch_files_from_http_post_data(request, 'files', context)

            if not content:
                context['err'] = 'محتوا بدرستی وارد نشده است'
                return render(request, 'panel/tickets/ticket-list.html', context)

            owner = ticket.owner
            receiver = ticket.receiver

            new_message = Message.objects.create(
                ticket=ticket,
                content=content,
                created_by=request.user,
            )

            for file in files:
                new_file = FileGallery.objects.create(
                    alt=file.name,
                    file=file,
                    created_by=request.user,
                )
                new_message.attachments.add(new_file)

            if request.user == owner:
                ticket.has_seen_by_owner = True
                ticket.has_seen_by_receiver = False
                ticket.status = 'owner_response'
            elif request.user == receiver:
                ticket.has_seen_by_owner = False
                ticket.has_seen_by_receiver = True
                ticket.status = 'receiver_response'
            else:
                ticket.has_seen_by_owner = False
                ticket.has_seen_by_receiver = False
                ticket.status = 'admin_response'
            ticket.save()

            context['message'] = f'پیام با موفقیت ایجاد گردید'
            return redirect('ticket:ticket-detail-with-id', ticket_id=ticket_id)
        except Exception as e:
            print(e)
            return render(request, 'panel/err/err-not-found.html')
