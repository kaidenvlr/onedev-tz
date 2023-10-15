# Generated by Django 4.2.6 on 2023-10-14 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_app', '0003_alter_user_django_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Placed'), (1, 'Pending'), (2, 'Finished')], default=0)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_app.user', verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='OrderImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='orders/', verbose_name='Картинка')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='order_app.order', verbose_name='Связанный заказ')),
            ],
        ),
    ]