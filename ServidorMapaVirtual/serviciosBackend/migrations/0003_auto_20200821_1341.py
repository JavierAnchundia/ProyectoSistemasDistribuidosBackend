# Generated by Django 3.1 on 2020-08-21 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviciosBackend', '0002_auto_20200821_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='red_social',
            name='nombre',
            field=models.CharField(max_length=15),
        ),
    ]
