from django.urls import path, include

from accounts.views import login_view, logout_view, signup_view, ProfileView

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),

    # Profile
    path('profile/profile-detail/', ProfileView().profile_detail, name='profile-detail'),
    path('profile/seller-profile-detail/', ProfileView().seller_profile_detail, name='seller-profile-detail'),
    path('profile/warehouse-profile-detail/', ProfileView().warehouse_profile_detail, name='warehouse-profile-detail'),
    path('profile/delivery-profile-detail/', ProfileView().delivery_profile_detail, name='delivery-profile-detail'),
    path('profile/profile-list/', ProfileView().list, name='profile-list'),
    path('profile/filter/', ProfileView().filter, name='profile-filter'),
    path('profile/create/', ProfileView().create, name='profile-create'),
    path('profile/profile-detail&id=<int:user_id>/', ProfileView().detail, name='profile-detail-with-id'),
    path('profile/profile-modify/', ProfileView().modify_profile, name='profile-modify'),
    path('profile/profile-seller-modify/', ProfileView().modify_seller_profile, name='profile-seller-modify'),
    path('profile/profile-warehouse-modify/', ProfileView().modify_warehouse_profile, name='profile-warehouse-modify'),
    path('profile/profile-delivery-modify/', ProfileView().modify_delivery_profile, name='profile-delivery-modify'),
    path('profile/profile-remove&id=<int:user_id>/', ProfileView().delete, name='profile-remove-with-id'),
]


