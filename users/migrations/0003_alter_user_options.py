# Generated by Django 3.2.15 on 2022-10-04 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_user_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': 'List of all Users'},
        ),
    ]
