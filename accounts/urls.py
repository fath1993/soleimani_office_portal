from django.urls import path

from accounts.views import login_view, logout_view, signup_view, ProfileView, PermissionView, RoleView

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

    # Permission
    path('permission/list/', PermissionView().list, name='permission-list'),
    path('permission/filter/', PermissionView().filter, name='permission-filter'),
    path('permission/create/', PermissionView().create, name='permission-create'),
    path('permission/detail&id=<int:permission_id>/', PermissionView().detail, name='permission-detail-with-id'),
    path('permission/modify&id=<int:permission_id>/', PermissionView().modify, name='permission-modify-with-id'),
    path('permission/delete&id=<int:permission_id>/', PermissionView().delete, name='permission-delete-with-id'),

    # Role
    path('role/list/', RoleView().list, name='role-list'),
    path('role/filter/', RoleView().filter, name='role-filter'),
    path('role/create/', RoleView().create, name='role-create'),
    path('role/detail&id=<int:role_id>/', RoleView().detail, name='role-detail-with-id'),
    path('role/modify&id=<int:role_id>/', RoleView().modify, name='role-modify-with-id'),
    path('role/delete&id=<int:role_id>/', RoleView().delete, name='role-delete-with-id'),
]


