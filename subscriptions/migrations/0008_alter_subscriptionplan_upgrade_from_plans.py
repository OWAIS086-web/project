# Generated by Django 3.2.16 on 2023-03-09 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0007_subscription_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='upgrade_from_plans',
            field=models.ManyToManyField(blank=True, to='subscriptions.SubscriptionPlan'),
        ),
    ]
