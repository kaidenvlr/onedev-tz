from django.db import models
from django.utils.crypto import get_random_string

from user_app.models import User


class OrderStatus(models.IntegerChoices):
    PLACED = 0, "Placed"
    PENDING = 1, "Pending"
    FINISHED = 2, "Finished"


class Order(models.Model):
    id = models.IntegerField(
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name="ID"
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    status = models.IntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.PLACED
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = get_random_string(length=6, allowed_chars='0123456789')
        return super(Order, self).save(*args, **kwargs)


class OrderImage(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Связанный заказ"
    )
    image = models.ImageField(
        upload_to=f'orders/',
        verbose_name="Картинка"
    )
