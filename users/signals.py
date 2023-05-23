from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import User


@receiver(pre_save, sender=User)
def model_user_pre_save(sender, instance, **kwargs):
    if not instance.name:
        instance.name = instance.get_full_name()


@receiver(post_save, sender=User)
def model_user_post_save(sender, created, instance, **kwargs):
    if created:
        # send_email_confirmation()
        pass
