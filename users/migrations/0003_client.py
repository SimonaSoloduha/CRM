# Generated by Django 4.1.4 on 2022-12-21 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0003_company_active_filter_one_time_zone_and_more'),
        ('users', '0002_code_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usser_id', models.CharField(max_length=155, verbose_name='usser_id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('status', models.CharField(blank=True, choices=[('NOT HAVE IN DB', 'NOT HAVE IN DB'), ('USER BAN', 'USER BAN'), ('DEVICE BANNED', 'DEVICE BANNED')], max_length=20, verbose_name='filter_two_cheker')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('сompany', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.company', verbose_name='сompany')),
            ],
            options={
                'verbose_name': 'clients',
                'verbose_name_plural': 'client',
            },
        ),
    ]