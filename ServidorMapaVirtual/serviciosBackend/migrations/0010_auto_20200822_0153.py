# Generated by Django 3.1 on 2020-08-22 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviciosBackend', '0009_merge_20200822_0150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camposanto',
            name='logo',
        ),
        migrations.AddField(
            model_name='empresa',
            name='logo',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to=''),
        ),
    ]