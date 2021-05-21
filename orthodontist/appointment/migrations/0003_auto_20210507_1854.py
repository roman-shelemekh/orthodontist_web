# Generated by Django 3.1.7 on 2021-05-07 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointment', '0002_auto_20210507_1604'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['date', 'time', 'clinic'], 'verbose_name': 'запись на прием', 'verbose_name_plural': 'Записи на прием'},
        ),
        migrations.AlterField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пациент'),
        ),
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together={('date', 'time')},
        ),
    ]
