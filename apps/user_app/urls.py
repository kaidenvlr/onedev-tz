from django.urls import path
from apps.user_app.views import login, get, change, register

urlpatterns = [
    path('get-user/', get.get_user, name='user_get'),
    path('get-users/', get.get_users, name='user_list'),

    path('change-user/', change.change_user_info, name='user_change_info'),
    path('change-avatar/', change.change_avatar, name='user_change_avatar'),
    path('change-password/', change.change_password, name='user_change_password'),

    path('register/', register.register, name='user_register'),
    path('login/', login.login, name='user_login'),
]
