from django.shortcuts import render
from accounts.custom_decorator import CheckLogin


class DashboardView:
    def __init__(self):
        super().__init__()

    @CheckLogin()
    def main(self, request, *args, **kwargs):
        context = {'page_title': 'پنل کاربری - داشبورد'}
        return render(request, 'panel/dashboard.html', context)