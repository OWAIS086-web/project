# Generated by Django 3.2.16 on 2022-12-22 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_auto_20221221_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='is_trial_period',
            field=models.BooleanField(default=False, verbose_name='Trial Period'),
        ),
        migrations.AddField(
            model_name='subscriptionplan',
            name='upgrade_from_plans',
            field=models.ManyToManyField(blank=True, related_name='_subscriptions_subscriptionplan_upgrade_from_plans_+', to='subscriptions.SubscriptionPlan'),
        ),
    ]
