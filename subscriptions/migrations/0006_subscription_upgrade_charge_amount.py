# Generated by Django 3.2.16 on 2022-12-22 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0005_auto_20221222_0657'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='upgrade_charge_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Upgrade Charge Amount'),
        ),
    ]
