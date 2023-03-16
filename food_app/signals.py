from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from .models import Customer


@receiver(user_signed_up)
def create_new_customer(request, user, **kwargs):
    customer = Customer.objects.create(user=user)
    return customer
