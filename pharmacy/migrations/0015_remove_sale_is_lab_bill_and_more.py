# Generated by Django 4.2.4 on 2023-09-18 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0014_sale_is_lab_bill_sale_lab_request_details_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='is_lab_bill',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='lab_request_details',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='patient',
        ),
    ]
