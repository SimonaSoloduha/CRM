# Generated by Django 4.1.4 on 2022-12-26 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_alter_log_filter_two_cheker'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='getr',
            field=models.CharField(default=123, max_length=255, verbose_name='getr'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='log',
            name='utm_medium',
            field=models.CharField(default='organic', max_length=255, verbose_name='utm_medium'),
        ),
    ]
