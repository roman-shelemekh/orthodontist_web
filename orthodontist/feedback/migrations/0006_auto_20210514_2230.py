# Generated by Django 3.1.7 on 2021-05-14 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_auto_20210514_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='email',
            field=models.EmailField(default='hello@tut.by', max_length=40, unique=True, verbose_name='Электронная почта'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedback',
            name='is_published',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='feedback',
            name='name',
            field=models.CharField(default='Roman', max_length=40, verbose_name='Имя'),
            preserve_default=False,
        ),
    ]