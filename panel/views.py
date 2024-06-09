from django.shortcuts import render, redirect
from accounts.custom_decorator import CheckLogin
from accounts.templatetags.account_custom_tag import has_access_to_section


class DashboardView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    def main(self, request, *args, **kwargs):
        if has_access_to_section(request, 'read,create,modify,delete,resource'):
            context = {'page_title': 'پنل کاربری - داشبورد'}
            return render(request, 'panel/dashboard.html', context)
        else:
            return redirect('automation:requested-product-processing-list')
