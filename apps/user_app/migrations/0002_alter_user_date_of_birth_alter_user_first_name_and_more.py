# Generated by Django 4.2.6 on 2023-10-13 09:41

from django.db import migrations, models
import apps.user_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(null=True, validators=[apps.user_app.validators.date_of_birth_validator], verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=12, null=True, validators=[
                apps.user_app.validators.phone_number_validator], verbose_name='Номер телефона'),
        ),
    ]
