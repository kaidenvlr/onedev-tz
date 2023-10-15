from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as DjangoUser

from apps.user_app.models import User


class UserInline(admin.StackedInline):
    model = User
    can_delete = False
    verbose_name_plural = "Пользователи"
    verbose_name = "Пользователь"


class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)


admin.site.unregister(DjangoUser)
admin.site.register(DjangoUser, UserAdmin)
