# Generated by Django 4.1.6 on 2023-04-11 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jewelry_site', '0004_contactdetail_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='is_selected',
            field=models.BooleanField(default=True),
        ),
    ]