# Generated by Django 3.1 on 2020-12-12 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviciosBackend', '0062_auto_20201206_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificaciones',
            fields=[
                ('id_notificacion', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=70)),
                ('descripcion', models.CharField(max_length=500)),
                ('fecha_created', models.DateField()),
                ('estado', models.CharField(choices=[('enviada', 'enviado'), ('no_enviada', 'no_enviado')], default='no_enviada', max_length=40)),
                ('id_camposanto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviciosBackend.camposanto')),
            ],
        ),
    ]