# Generated by Django 3.1 on 2020-12-03 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviciosBackend', '0059_auto_20201125_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paquetes',
            fields=[
                ('id_paquete', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=70)),
                ('descripcion', models.CharField(max_length=200)),
                ('precio', models.FloatField()),
                ('imagen', models.ImageField(blank=True, max_length=200, null=True, upload_to='paquetes')),
                ('fecha_created', models.DateField()),
                ('estado', models.BooleanField(default=True)),
                ('id_camposanto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviciosBackend.camposanto')),
            ],
        ),
    ]
