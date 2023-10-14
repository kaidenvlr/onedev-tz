from django.urls import path
from user_app.views import login, register, basic

urlpatterns = [
    path('get-user/', basic.get_user, name='user_get'),
    path('get-users/', basic.get_users, name='user_list'),

    path('change-user/', basic.change_user_info, name='user_change_info'),
    path('change-avatar/', basic.change_avatar, name='user_change_avatar'),

    path('register/', register.register, name='user_register'),
    path('login/', login.login, name='user_login'),
]
