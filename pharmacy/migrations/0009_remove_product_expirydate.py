# Generated by Django 4.2.4 on 2023-09-17 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0008_rename_birth_cerificate_or_id_patient_phone_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='expirydate',
        ),
    ]
