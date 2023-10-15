from django.contrib import admin
from django.utils.translation import ngettext

from order_app.models import Order
from tasks.status import change_status


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status"]
    search_fields = ["user"]
    list_filter = ["status"]
    actions = ["task"]

    @admin.action(description='Make orders as "Finished"')
    def task(self, request, queryset):
        self.message_user(
            request,
            ngettext(
                "%d order status changed to Pending",
                "%d orders status changed to Pending",
                len(queryset)
            )
        )
        change_status.run(queryset)
        self.message_user(
            request,
            ngettext(
                "%d order status changed to Finished",
                "%d orders status changed to Finished",
                len(queryset)
            )
        )
