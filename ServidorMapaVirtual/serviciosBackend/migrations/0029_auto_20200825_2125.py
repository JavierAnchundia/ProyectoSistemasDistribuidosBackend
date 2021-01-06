# Generated by Django 3.1 on 2020-08-26 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviciosBackend', '0028_auto_20200825_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tipo_usuario',
            field=models.CharField(choices=[('su', 'super_admin'), ('ad', 'admin'), ('uf', 'usuario_final'), ('ha', 'hiper_admin')], default='ad', max_length=30),
        ),
    ]