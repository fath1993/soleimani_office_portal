from django.contrib import admin
from account.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'first_name',
        'last_name',
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
    )

    def has_add_permission(self, request):
        return False

