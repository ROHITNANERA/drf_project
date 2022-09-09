# Generated by Django 4.0.6 on 2022-07-27 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_patient_hospital'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='hospital',
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name', models.CharField(max_length=30)),
                ('doctor_speciality', models.CharField(max_length=30)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.hospital')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.doctor'),
        ),
    ]