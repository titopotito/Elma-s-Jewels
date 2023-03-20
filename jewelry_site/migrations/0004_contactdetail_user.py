# Generated by Django 4.1.6 on 2023-02-13 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jewelry_site', '0003_contactdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactdetail',
            name='user',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]