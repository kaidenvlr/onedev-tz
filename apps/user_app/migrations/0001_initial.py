# Generated by Django 4.2.6 on 2023-10-13 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import apps.user_app.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12, validators=[
                    apps.user_app.validators.phone_number_validator], verbose_name='Номер телефона')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar/', verbose_name='Аватар пользователя')),
                ('date_of_birth', models.DateField(validators=[apps.user_app.validators.date_of_birth_validator], verbose_name='Дата рождения')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('django_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
