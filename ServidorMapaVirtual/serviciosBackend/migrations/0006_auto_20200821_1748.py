# Generated by Django 3.1 on 2020-08-21 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviciosBackend', '0005_auto_20200821_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='punto_geolocalizacion',
            name='id_camposanto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviciosBackend.camposanto'),
        ),
    ]
