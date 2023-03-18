from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer


@receiver(post_save, sender=User)
def create_new_customer(sender, instance, created, *args, **kwargs):
    if created:
        customer = Customer.objects.create(user=instance)
        return customer
