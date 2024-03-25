from django.urls import path
from account.views import login_view, logout_view, Account

app_name = 'accounts'

urlpatterns = (
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # profile
    path('api/profile/', Account.as_view(), name='profile'),
)


