from django.db import migrations, models

def populate_pnumber(apps, schema_editor):
    Patient = apps.get_model('pharmacy', 'Patient')
    for index, patient in enumerate(Patient.objects.all(), start=1):
        patient.pnumber = f'P{index:04d}'  # You can adjust the format as needed
        patient.save()

class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0027_patient_patient_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='pnumber',
            field=models.CharField(max_length=100, unique=True, null=True, blank=True),
        ),
        migrations.RunPython(populate_pnumber),
    ]
