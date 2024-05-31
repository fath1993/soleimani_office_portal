import random

from django.contrib.auth.models import User

from accounts.models import Role, SellerProfile


def create_test_account():
    print('input number of accounts')
    number_of_accounts = int(input())
    for i in range(0, number_of_accounts):
        username = f'{random.randint(99999999, 999999999)}'
        email = f'email.{random.randint(9999, 99999)}@junkmail.com'
        password = 'amir1372'

        new_user = User.objects.create_user(
            username=username,
            email=email,
        )
        new_user.set_password(password)
        new_user.save()
        profile = new_user.user_profile

        profile.first_name = f'first_name_{random.randint(99999999, 999999999)}'
        profile.last_name = f'last_name_{random.randint(99999999, 999999999)}'
        profile.national_code = f'{random.randint(9999999999, 99999999999)}'
        profile.mobile_phone_number = f'{random.randint(9999999999, 99999999999)}'
        profile.landline = f'021{random.randint(9999999, 99999999)}'
        profile.card_number = f'{random.randint(9999999999, 99999999999)}'
        profile.isbn = f'{random.randint(9999999999, 99999999999)}'
        profile.address = f'tehran_{random.randint(9999999999, 99999999999)}'

        roles = Role.objects.all()
        profile.role = random.choice(roles)
        profile.save()

        seller_profiles = SellerProfile.objects.get(profile=profile)
        if seller_profiles.sale_allowance:
            seller_profiles.daily_allowed_product_processing_number = f'{random.randint(0, 100)}'
            seller_profiles.save()


def set_user_password():
    for user in User.objects.all():
        password = 'amir1372'
        user.set_password(password)
        user.save()