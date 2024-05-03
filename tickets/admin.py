from django.contrib import admin

from tickets.models import Ticket, Message, Notification


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'status',
        'subject',
        'owner',
        'receiver',
        'has_seen_by_owner',
        'has_seen_by_receiver',
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
        'subject',
        'owner',
        'receiver',
        'has_seen_by_owner',
        'has_seen_by_receiver',
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


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'content',
        'created_at',
        'created_by',
    )

    readonly_fields = (
        'created_at',
        'created_by',
    )

    fields = (
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
