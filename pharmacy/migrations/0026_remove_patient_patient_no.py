# Generated by Django 4.2.4 on 2023-10-05 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0025_patient_patient_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='patient_no',
        ),
    ]