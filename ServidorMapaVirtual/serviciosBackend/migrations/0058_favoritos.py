
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviciosBackend', '0057_tokendevice_plataform'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favoritos',
            fields=[
                ('id_favorito', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('estado', models.BooleanField(default=False)),
                ('id_difunto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviciosBackend.difunto')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
