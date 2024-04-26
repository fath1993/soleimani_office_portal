from django.contrib import admin

from tickets.models import Ticket, Message


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'status',
        'title',
        'has_seen_by_user',
        'belong_to',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    fields = (
        'status',
        'title',
        'has_seen_by_user',
        'belong_to',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    def save_model(self, request, instance, form, change):
        instance = form.save(commit=False)
        if not change:
            instance.created_by = request.user
            instance.updated_by = request.user
            instance.status = 'ایجاد شده'
        else:
            instance.updated_by = request.user
        instance.save()
        form.save_m2m()
        user_profile = instance.belong_to.user_profile
        unseen_tickets = Ticket.objects.filter(belong_to=instance.belong_to, has_seen_by_user=False)
        user_profile.unseen_ticket_number = unseen_tickets.count()
        user_profile.save()
        return instance


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'ticket',
        'content',
        'created_at',
        'created_by',
    )

    readonly_fields = (
        'created_at',
        'created_by',
    )

    fields = (
        'ticket',
        'content',
        'attachments',
        'created_at',
        'created_by',
    )

    def save_model(self, request, instance, form, change):
        instance = form.save(commit=False)
        if not change:
            instance.created_by = request.user
        instance.save()
        form.save_m2m()
        return instance
