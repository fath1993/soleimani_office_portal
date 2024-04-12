from django.urls import path

from panel.views import DashboardView, UserView, PermissionView, RoleView

app_name = 'panel'

urlpatterns = [
    path('', DashboardView().main, name='panel-dashboard'),

    # User
    path('user/user-list/', UserView().list, name='user-list'),
    path('user/filter/', UserView().filter, name='user-filter'),
    path('user/create/', UserView().create, name='user-create'),
    path('user/user-detail&id=<int:user_id>/', UserView().detail, name='user-detail-with-id'),
    path('user/user-edit&id=<int:user_id>/', UserView().modify, name='user-edit-with-id'),
    path('user/user-remove&id=<int:user_id>/', UserView().delete, name='user-remove-with-id'),

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
