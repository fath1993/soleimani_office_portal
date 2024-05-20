from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME

from accounts.models import Profile, Permission, Role, UserNotification, SellerProfile, Section, SECTIONS, \
    create_permissions, create_sections, create_roles, update_sections, update_permissions, DeliveryProfile, \
    WarehouseProfile


# @admin.register(Section)
# class SectionAdmin(admin.ModelAdmin):
#     list_display = (
#         'name_fa',
#     )
#
#     readonly_fields = (
#         'name',
#         'name_fa',
#     )
#
#     fields = (
#         'name',
#         'name_fa',
#     )
#
#     actions = (
#         'recreate_sections',
#     )
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def changelist_view(self, request, extra_context=None):
#         if 'action' in request.POST and request.POST['action'] == 'recreate_sections':
#             if not request.POST.getlist(ACTION_CHECKBOX_NAME):
#                 post = request.POST.copy()
#                 for u in Section.objects.all():
#                     post.update({ACTION_CHECKBOX_NAME: str(u.id)})
#                 request._set_post(post)
#         return super(SectionAdmin, self).changelist_view(request, extra_context)
#
#     @admin.action(description='بازسازی بخش ها، اجازه ها و نقش های سیستم')
#     def recreate_sections(self, request, queryset):
#         update_sections()
#         update_permissions()
#         create_roles()



# @admin.register(Permission)
# class PermissionAdmin(admin.ModelAdmin):
#     list_display = (
#         'has_access_to_section',
#         'has_access_to_section_display',
#         'read',
#         'create',
#         'modify',
#         'delete',
#     )
#
#     list_filter = (
#         'has_access_to_section',
#         'read',
#         'create',
#         'modify',
#         'delete',
#     )
#
#     search_fields = (
#         'has_access_to_section__name',
#     )
#
#     fields = (
#         'has_access_to_section',
#         'read',
#         'create',
#         'modify',
#         'delete',
#     )
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     @admin.display(description="اجازه های صادر شده", empty_value='???')
#     def has_access_to_section_display(self, obj):
#         string = f''''''
#         if obj.read:
#             string += 'read, '
#         if obj.create:
#             string += 'create, '
#         if obj.modify:
#             string += 'modify, '
#         if obj.delete:
#             string += 'delete, '
#         return string



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

    list_filter = (
        'role',
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


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'profile',
        'daily_allowed_product_processing_number',
    )

    readonly_fields = (
        'profile',
    )

    fields = (
        'profile',
        'daily_allowed_product_processing_number',
    )

    def has_add_permission(self, request):
        return False


@admin.register(WarehouseProfile)
class WarehouseProfileAdmin(admin.ModelAdmin):
    list_display = (
        'profile',
    )

    readonly_fields = (
        'profile',
    )

    fields = (
        'profile',
    )

    def has_add_permission(self, request):
        return False


@admin.register(DeliveryProfile)
class DeliveryProfileAdmin(admin.ModelAdmin):
    list_display = (
        'profile',
    )

    readonly_fields = (
        'profile',
    )

    fields = (
        'profile',
    )

    def has_add_permission(self, request):
        return False


admin.site.register(UserNotification)


