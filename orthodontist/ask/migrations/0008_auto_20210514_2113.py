# Generated by Django 3.1.7 on 2021-05-14 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0007_auto_20210507_0819'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'ответ', 'verbose_name_plural': 'ответы'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'вопрос', 'verbose_name_plural': 'вопросы'},
        ),
    ]
