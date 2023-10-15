import time

from celery import shared_task

from order_app.models import Order


@shared_task
def change_status(queryset):
    queryset.update(status=1)
    time.sleep(10)
    queryset.update(status=2)
    return True
