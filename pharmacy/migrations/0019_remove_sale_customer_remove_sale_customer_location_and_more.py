# Generated by Django 4.2.4 on 2023-09-20 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0018_sale_is_lab_bill_sale_lab_request_details_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='customer_location',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='customer_number',
        ),
    ]
