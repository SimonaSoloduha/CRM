# Generated by Django 4.1.4 on 2022-12-14 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='country',
            new_name='name',
        ),
    ]
