# Generated by Django 4.1.6 on 2023-02-09 13:35

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jewelry_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]
