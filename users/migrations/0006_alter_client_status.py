# Generated by Django 4.1.4 on 2022-12-26 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_client_сompany'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.CharField(blank=True, choices=[('NOT HAVE IN DB', 'NOT HAVE IN DB'), ('USER BAN', 'USER BAN'), ('DEVICE BANNED', 'DEVICE BANNED'), ('RETRY USER', 'RETRY USER')], max_length=20, verbose_name='status'),
        ),
    ]