# Generated by Django 5.0.2 on 2024-02-25 19:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='last login'),
            preserve_default=False,
        ),
    ]