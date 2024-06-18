# Generated by Django 5.0.4 on 2024-06-18 09:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_useremailstatus'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useremailstatus',
            options={'verbose_name_plural': 'User email statuses'},
        ),
        migrations.AlterField(
            model_name='useremailstatus',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='email_status', to=settings.AUTH_USER_MODEL),
        ),
    ]