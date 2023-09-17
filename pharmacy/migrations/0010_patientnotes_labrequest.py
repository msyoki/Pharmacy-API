# Generated by Django 4.2.4 on 2023-09-17 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0009_remove_product_expirydate'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(max_length=300)),
                ('captured', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.patient')),
            ],
        ),
        migrations.CreateModel(
            name='LabRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300)),
                ('billed_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('captured', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.patient')),
            ],
        ),
    ]
