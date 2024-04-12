from django.contrib import admin
from accounts.models import Profile, Permission, Role


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'has_access_to_section',
        'read',
        'create',
        'modify',
        'delete',
    )

    list_filter = (
        'has_access_to_section',
        'read',
        'create',
        'modify',
        'delete',
    )

    search_fields = (
        'title',
    )

    fields = (
        'title',
        'has_access_to_section',
        'read',
        'create',
        'modify',
        'delete',
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )

    search_fields = (
        'title',
    )

    fields = (
        'title',
        'permissions',
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'first_name',
        'last_name',
        'role',
    )

    readonly_fields = (
        'user',
    )

    fields = (
        'user',
        'first_name',
        'last_name',
        'national_code',
        'mobile_phone_number',
        'landline',
        'birthday',
        'card_number',
        'isbn',
        'address',
        'role',
    )

    def has_add_permission(self, request):
        return False