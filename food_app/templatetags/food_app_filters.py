from datetime import timedelta

from django import template
from django.utils import timezone

register = template.Library()


@register.filter()
def add_days(days):
    new_date = timezone.now() + timedelta(days=days)
    return new_date
