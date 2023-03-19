from datetime import timedelta
import random
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer, Recipe, Subscription, Menu


@receiver(post_save, sender=User)
def create_new_customer(sender, instance, created, *args, **kwargs):
    if created:
        customer = Customer.objects.create(user=instance)
        return customer


@receiver(post_save, sender=Subscription)
def create_menu_items(sender, instance, created, update_fields, **kwargs):
    if (created or (update_fields and 'is_active' in update_fields)) and instance.is_active:
        plan = instance.plan

        recipes = Recipe.objects.filter(
            category=plan.recipe_category,
            food_intake__in=plan.food_intakes.all(),
        ).exclude(allergic_categories__in=plan.allergies.all())

        food_intakes = plan.food_intakes.all()
        recipes = Recipe.objects.filter(
            category=plan.recipe_category,
            food_intake__in=food_intakes,
        ).exclude(allergic_categories__in=plan.allergies.all())

        menu_items = []
        for food_intake in food_intakes:

            current_date = instance.start
            food_intake_recipes = recipes.filter(food_intake=food_intake).all()

            while current_date <= instance.end:
                menu_items.append(
                    Menu(
                        date=current_date,
                        recipe=random.choice(food_intake_recipes),
                        subscription=instance
                    )
                )
                current_date += timedelta(days=1)

        Menu.objects.bulk_create(menu_items)
