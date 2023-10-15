from django.contrib import admin

from order_app.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status"]
    search_fields = ["user"]
    list_filter = ["status"]
