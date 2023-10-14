import datetime

from django.contrib.auth.models import User as DjangoUser
from django.db import models
from django.db.models.signals import post_save

from user_app.validators import phone_number_validator, date_of_birth_validator


class User(models.Model):
    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, validators=(phone_number_validator,), verbose_name="Номер телефона",
                                    null=True)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True, verbose_name="Аватар пользователя")
    date_of_birth = models.DateField(validators=[date_of_birth_validator], verbose_name="Дата рождения", null=True)
    first_name = models.CharField(max_length=100, verbose_name="Имя", null=True)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.phone_number}"


def create_user(sender, instance, created, **kwargs):
    if created:
        user_profile = User(django_user=instance)
        user_profile.save()


post_save.connect(create_user, sender=DjangoUser)
