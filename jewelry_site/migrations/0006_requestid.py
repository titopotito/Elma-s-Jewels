# Generated by Django 4.1.6 on 2023-04-12 10:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('jewelry_site', '0005_cartitem_is_selected'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestID',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
    ]
