# Generated by Django 4.0.6 on 2022-07-25 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h_name', models.CharField(max_length=50)),
                ('h_address', models.CharField(max_length=80)),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='hospital',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='patients', to='myapp.hospital'),
            preserve_default=False,
        ),
    ]
