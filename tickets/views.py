import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_safe, require_POST
from django.shortcuts import render, redirect
from accounts.models import Profile
from gallery.models import FileGallery
from panel.views import CheckLogin, CheckPermissions
from django.core.files.base import File

from tickets.models import Ticket, Message
from tickets.serializer import MessageSerializer
from tickets.templatetags.tickets_custom_tag import ticket_admin_is_allowed
from utilities.http_metod import fetch_data_from_http_post, fetch_single_file_from_http_files, \
    fetch_files_from_http_post_data


class TicketView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست تیکت های من', 'get_params': request.GET.urlencode()}
        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست تیکت های من شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        q &= (
            Q(**{'belong_to': request.user})
        )
        if search:
            q &= (
                Q(**{'title__icontains': search})
            )
        tickets = Ticket.objects.filter(q).order_by('-created_at')

        items_per_page = 50
        paginator = Paginator(tickets, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/tickets/ticket-list.html', context)

    @CheckLogin()
    def detail(self, request, ticket_id, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            messages = Message.objects.filter(ticket=ticket)
            if ticket.belong_to != request.user:
                return render(request, 'panel/err/err-not-authorized.html')
            context = {'page_title': f'اطلاعات تیکت *{ticket.title}*',
                       'ticket': ticket, 'messages': messages, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/tickets/ticket-detail.html', context)
        except Exception as e:
            print(e)
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست تیکت های من شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        q &= (
            Q(**{'belong_to': request.user})
        )
        if search:
            q &= (
                Q(**{'title__icontains': search})
            )
        tickets = Ticket.objects.filter(q)

        items_per_page = 50
        paginator = Paginator(tickets, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/tickets/ticket-list.html', context)

    @CheckLogin()
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت تیکت جدید', 'get_params': request.GET.urlencode()}

        title = fetch_data_from_http_post(request, 'title', context)
        content = fetch_data_from_http_post(request, 'content', context)
        files = fetch_files_from_http_post_data(request, 'files', context)

        if not title:
            context['err'] = 'عنوان بدرستی وارد نشده است'
            return render(request, 'panel/tickets/ticket-list.html', context)

        new_ticket = Ticket.objects.create(
            title=title,
            belong_to=request.user,
            created_by=request.user,
            updated_by=request.user,
        )

        new_message = Message.objects.create(
            ticket=new_ticket,
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

        context['message'] = f'تیکت با عنوان {title} ایجاد گردید'
        return redirect('ticket:ticket-list')

    @CheckLogin()
    def close(self, request, ticket_id, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            context = {'page_title': f'بستن تیکت *{ticket.title}*',
                       'ticket': ticket, 'get_params': request.GET.urlencode()}
            ticket.status = 'closed'
            ticket.save()
            return redirect('ticket:ticket-list')
        except:
            return render(request, 'panel/err/err-not-found.html')


class TicketAdminView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='read')
    def list(self, request, *args, **kwargs):
        context = {'page_title': 'لیست تیکت ها', 'get_params': request.GET.urlencode()}
        search = request.GET.get('search')
        if search:
            context = {'page_title': f'لیست نقش ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                Q(**{'title__icontains': search})
            )

        if ticket_is_allowed(request.user,
                             allowed_actions='modify,delete'):  # The admin user who manage tickets should have these rights
            tickets = TicketChatBox.objects.all().order_by('-created_at')
        else:
            tickets = TicketChatBox.objects.filter(user=request.user).order_by('-created_at')

        context['tickets'] = tickets
        items_per_page = 50
        paginator = Paginator(tickets, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/tickets/ticket-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='read')
    def detail(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'اطلاعات نقش *{role.title}*',
                       'role': role, 'get_params': request.GET.urlencode()}
            return render(request, 'panel/roles/role-detail.html', context)
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='read')
    def filter(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {'page_title': f'لیست نقش ها شامل *{search}*', 'get_params': request.GET.urlencode()}

        q = Q()
        if search:
            q &= (
                Q(**{'title__icontains': search})
            )
        roles = Role.objects.filter(q).order_by('id')
        context['roles'] = roles

        items_per_page = 50
        paginator = Paginator(roles, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context['page'] = page

        return render(request, 'panel/roles/role-list.html', context)

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='create')
    def create(self, request, *args, **kwargs):
        context = {'page_title': 'ساخت تیکت جدید', 'get_params': request.GET.urlencode()}

        user_id = fetch_data_from_http_post(request, 'user_id', context)
        title = fetch_data_from_http_post(request, 'title', context)
        department = fetch_data_from_http_post(request, 'department', context)
        message = fetch_data_from_http_post(request, 'message', context)
        file = fetch_single_file_from_http_files(request, 'file', context)

        if not title:
            context['err'] = 'عنوان بدرستی وارد نشده است'
            return render(request, 'panel/tickets/ticket-list.html', context)
        if not user_id:  # it meant it create by user
            ticket_belong_to = User.objects.get(id=request.user.id)
            receiver = User.objects.get(username='admin')
        else:  # it meant it create by admin
            ticket_belong_to = User.objects.get(username='admin')
            receiver = User.objects.get(id=user_id)

        TicketChatBox.objects.create(
            user=User.objects.get(id=user_id),
            title=title,
            department=department,
            ticket_state="ایجاد شده",
        )

        MessageContent.objects.create(
            creator=creator,
            receiver=receiver,
            message=message,
            file=file,
        )

        context['message'] = f'مجوز با عنوان {title} ایجاد گردید'
        return redirect('panel:role-list')

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='modify')
    def modify(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'ویرایش اطلاعات نقش *{role.title}*',
                       'permission': role, 'get_params': request.GET.urlencode()}
            if request.method == 'GET':
                return render(request, 'panel/roles/role-edit.html', context)
            else:
                title = fetch_data_from_http_post(request, 'first_name', context)
                has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
                read = fetch_data_from_http_post(request, 'national_code', context)
                create = fetch_data_from_http_post(request, 'email', context)
                modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
                delete = fetch_data_from_http_post(request, 'landline', context)

                if not title:
                    context['err'] = 'عنوان بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if not has_access_to_section:
                    context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if read == 'true':
                    read = True
                else:
                    read = False
                if create == 'true':
                    create = True
                else:
                    create = False
                if modify == 'true':
                    modify = True
                else:
                    modify = False
                if delete == 'true':
                    delete = True
                else:
                    delete = False

                if title:
                    role.title = title
                if has_access_to_section:
                    role.has_access_to_section = has_access_to_section

                if read:
                    role.read = read
                if create:
                    role.create = create
                if modify:
                    role.modify = modify
                if delete:
                    role.delete = delete

                role.save()
                context['message'] = f'مجوز با عنوان {title} ویرایش گردید'
                return redirect(
                    reverse('panel:role-modify-with-id',
                            kwargs={'role_id': role_id}) + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='modify')
    def close(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'ویرایش اطلاعات نقش *{role.title}*',
                       'permission': role, 'get_params': request.GET.urlencode()}
            if request.method == 'GET':
                return render(request, 'panel/roles/role-edit.html', context)
            else:
                title = fetch_data_from_http_post(request, 'first_name', context)
                has_access_to_section = fetch_data_from_http_post(request, 'last_name', context)
                read = fetch_data_from_http_post(request, 'national_code', context)
                create = fetch_data_from_http_post(request, 'email', context)
                modify = fetch_data_from_http_post(request, 'mobile_phone_number', context)
                delete = fetch_data_from_http_post(request, 'landline', context)

                if not title:
                    context['err'] = 'عنوان بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if not has_access_to_section:
                    context['err'] = 'بخش دسترسی بدرستی وارد نشده است'
                    return render(request, 'panel/permissions/permission-edit.html', context)
                if read == 'true':
                    read = True
                else:
                    read = False
                if create == 'true':
                    create = True
                else:
                    create = False
                if modify == 'true':
                    modify = True
                else:
                    modify = False
                if delete == 'true':
                    delete = True
                else:
                    delete = False

                if title:
                    role.title = title
                if has_access_to_section:
                    role.has_access_to_section = has_access_to_section

                if read:
                    role.read = read
                if create:
                    role.create = create
                if modify:
                    role.modify = modify
                if delete:
                    role.delete = delete

                role.save()
                context['message'] = f'مجوز با عنوان {title} ویرایش گردید'
                return redirect(
                    reverse('panel:role-modify-with-id',
                            kwargs={'role_id': role_id}) + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')

    @CheckLogin()
    @CheckPermissions(section='ticket', allowed_actions='delete')
    def delete(self, request, role_id, *args, **kwargs):
        try:
            role = Role.objects.get(id=role_id)
            context = {'page_title': f'حذف نقش {role.title}', 'get_params': request.GET.urlencode()}
            role.delete()
            return redirect(reverse('panel:role-list') + f'?{request.GET.urlencode()}')
        except:
            return render(request, 'panel/err/err-not-found.html')



class MessageView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    def list(self, request, ticket_id, *args, **kwargs):
        messages = Message.objects.filter(ticket__id=ticket_id)

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
            if not ticket_admin_is_allowed(request.user, allowed_actions='read'):
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
            ticket = Ticket.objects.get(id=ticket_id)
            if not ticket_admin_is_allowed(request.user, allowed_actions='read'):
                if ticket.belong_to != request.user:
                    return render(request, 'panel/err/err-not-authorized.html')

            context = {'page_title': f'ساخت پیام جدید ذیل تیکت {ticket_id}', 'get_params': request.GET.urlencode()}

            content = fetch_data_from_http_post(request, 'content', context)
            files = fetch_files_from_http_post_data(request, 'files', context)

            if not content:
                context['err'] = 'محتوا بدرستی وارد نشده است'
                return render(request, 'panel/tickets/ticket-list.html', context)

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

            context['message'] = f'پیام با موفقیت ایجاد گردید'
            return redirect('ticket:ticket-detail-with-id', ticket_id=ticket_id)
        except Exception as e:
            print(e)
            return render(request, 'panel/err/err-not-found.html')



@login_required
@require_GET
def ticket_list(request):
    if request.user.is_authenticated:
        context = {'page_title': 'لیست تیکت ها', 'profile': Profile.objects.get(user=request.user)}
        if request.user.is_superuser or request.user.is_staff:
            tickets = TicketChatBox.objects.all().order_by('-created_at')
        else:
            tickets = TicketChatBox.objects.filter(user=request.user).order_by('-created_at')
        context['tickets'] = tickets
        return render(request, 'panel/tickets/ticket-list.html', context)
    else:
        return redirect('accounts:static-login')


@login_required
def new_ticket(request):
    context = {'page_title': 'ارسال تیکت جدید', 'profile': Profile.objects.get(user=request.user)}
    if request.method == 'POST':
        try:
            chat_box_title = request.POST['chat_box_title']
            if chat_box_title == '':
                chat_box_title = None
        except:
            chat_box_title = None
        try:
            receiver = request.POST['receiver']
            if receiver == '':
                receiver = None
        except:
            receiver = None
        if receiver == 1:
            receiver = 'پشتیبانی فنی'
        elif receiver == 2:
            receiver = 'امور مالی'
        else:
            receiver = 'ارسال مدرک'

        try:
            message = request.POST['message']
            if chat_box_title == '':
                message = None
        except:
            message = None
        try:
            file = request.FILES['file']
            if file == '':
                file = None
        except:
            file = None

        new_ticket_box = TicketChatBox(
            user=request.user,
            title=chat_box_title,
            receiever=receiver,
        )
        new_ticket_box.save()

        new_message_content = MessageContent(
            creator=request.user,
            receiver=User.objects.get(username='admin'),
            message=message,
        )
        new_message_content.save()
        if file is not None:
            now = datetime.datetime.now()
            fs = FileSystemStorage(location='media/user-ticket-attachment/')
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            with open(file_path, 'rb') as f:
                new_message_content.file.save(str(request.user.username) + "-" + str(now.date()) + "-" + str(filename),
                                              File(f))
                f.close()
                new_message_content.save()
        new_ticket_box.message_box.add(new_message_content)
        new_ticket_box.save()
        admin = User.objects.get(username='admin')
        send_sms_to_superadmin(admin.mobile_phone_number)
        tickets = TicketChatBox.objects.filter(user=request.user).order_by('created_at')
        context['tickets'] = tickets
        return redirect('ticket:ticket-list')

    return render(request, 'panel/tickets/ticket-new.html', context)


@login_required
def ticket_chat_box(request, chat_id):
    context = {'page_title': 'صفحه تبادل پیام', 'profile': Profile.objects.get(user=request.user)}
    if request.method == 'POST':
        try:
            message = request.POST['message']
            if message == '':
                message = None
        except:
            message = None
        try:
            file = request.FILES['file']
            if file == '':
                file = None
        except:
            file = None
        new_message_content = MessageContent(
            creator=request.user,
            receiver=User.objects.get(username='admin'),
            message=message,
        )
        new_message_content.save()
        if file is not None:
            now = datetime.datetime.now()
            fs = FileSystemStorage(location='media/user-ticket-attachment/')
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            with open(file_path, 'rb') as f:
                new_message_content.file.save(str(request.user.username) + "-" + str(now.date()) + "-" + str(filename),
                                              File(f))
                f.close()
                new_message_content.save()
        ticket_box = TicketChatBox.objects.get(id=chat_id)
        ticket_box.ticket_stage = "پاسخ کاربر"
        ticket_box.message_box.add(new_message_content)
        ticket_box.save()
        return redirect('ticket:ticket-chat-box', chat_id=chat_id)
    ticket_box = TicketChatBox.objects.get(id=chat_id)
    context['ticket_box'] = ticket_box
    return render(request, 'panel/tickets/ticket-chat-box.html', context)


@login_required
@require_POST
@csrf_exempt
def ajax_close_ticket(request):
    try:
        chat_id = request.POST['chat_id']
        if chat_id == '':
            chat_id = None
    except:
        chat_id = None
    ticket_box = TicketChatBox.objects.get(id=chat_id)
    ticket_box.ticket_stage = "بسته شده"
    ticket_box.save()
    return HttpResponse('OK')


def send_sms_to_superadmin(phone_number):
    try:
        api_key = "Rsibe_LPzQjjNySv1zWN-qZLFwD_-yfa0ukc-6lkFps="
        pid = '8n08mk7jofdk6yf'
        url = 'http://ippanel.com:8080/?apikey=' + str(api_key) + '&pid=' + str(pid) + '&fnum=3000505&tnum=' + \
              str(phone_number) + '&p1=admin&v1=' + str(phone_number)
        print(url)
        requests.get(url, timeout=5)
        return True
    except Exception as e:
        print(e)
        return False
