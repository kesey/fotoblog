# Generated by Django 4.1.7 on 2023-04-07 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('CREATOR', 'Créateur'), ('SUBSCRIBER', 'Abonné')], max_length=30, verbose_name='Rôle'),
        ),
    ]
