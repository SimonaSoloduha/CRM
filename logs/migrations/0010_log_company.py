# Generated by Django 4.1.4 on 2022-12-30 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_alter_company_managers'),
        ('logs', '0009_alter_log_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='companies.company', verbose_name='company'),
        ),
    ]
