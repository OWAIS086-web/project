from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Subscription


@receiver(pre_save, sender=Subscription)
def model_subscription_pre_save(sender, instance, **kwargs):
    if not instance.pk and instance.plan:
        instance.title = instance.plan.title
        instance.description = instance.plan.description
    if instance.pk and instance.plan:
        if instance.title is None or instance.title == '':
            instance.title = instance.plan.title
        if instance.description is None or instance.description == '':
            instance.description = instance.plan.description

