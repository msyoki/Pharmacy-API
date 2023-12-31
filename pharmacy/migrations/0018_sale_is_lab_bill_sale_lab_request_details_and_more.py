# Generated by Django 4.2.4 on 2023-09-18 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0017_remove_sale_is_lab_bill_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='is_lab_bill',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sale',
            name='lab_request_details',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pharmacy.patient'),
        ),
    ]
