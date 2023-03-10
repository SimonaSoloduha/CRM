# Generated by Django 4.1.4 on 2022-12-21 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_alter_company_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='active_filter_one_time_zone',
            field=models.BooleanField(default=False, verbose_name='active_filter_one_time_zone'),
        ),
        migrations.AddField(
            model_name='company',
            name='filter_two_cheker',
            field=models.BooleanField(default=False, verbose_name='active_filter_one_time_zone'),
        ),
        migrations.AddField(
            model_name='company',
            name='url_response',
            field=models.CharField(blank=True, max_length=155, verbose_name='url_response'),
        ),
        migrations.AlterField(
            model_name='company',
            name='notificator',
            field=models.CharField(blank=True, max_length=255, verbose_name='notificator'),
        ),
    ]
