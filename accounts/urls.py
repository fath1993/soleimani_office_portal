from django.urls import path, include

from accounts.views import login_view, logout_view, signup_view, ProfileView

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),

    # Profile
    path('profile/profile-list/', ProfileView().list, name='profile-list'),
    path('profile/filter/', ProfileView().filter, name='profile-filter'),
    path('profile/create/', ProfileView().create, name='profile-create'),
    path('profile/profile-detail&id=<int:user_id>/', ProfileView().detail, name='profile-detail-with-id'),
    path('profile/profile-edit&id=<int:user_id>/', ProfileView().modify, name='profile-edit-with-id'),
    path('profile/profile-remove&id=<int:user_id>/', ProfileView().delete, name='profile-remove-with-id'),
]
