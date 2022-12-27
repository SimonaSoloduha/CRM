# Generated by Django 4.1.4 on 2022-12-14 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('countries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155, verbose_name='name')),
                ('domen', models.CharField(max_length=155, verbose_name='domen')),
                ('notificator', models.CharField(max_length=155, verbose_name='notificator')),
                ('countries', models.ManyToManyField(related_name='company', to='countries.country', verbose_name='countries')),
            ],
        ),
    ]