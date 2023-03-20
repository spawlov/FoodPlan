import random

from django.db.models import Count, Sum, F
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone

from yookassa import Payment

from calendar import mdays
from datetime import datetime, timedelta
import uuid

from food_app.forms import OrderForm, PaymentForm
from .models import Customer, Menu, Plan, Promocode, Recipe, Subscription


def index(request):
    return render(request, 'food_app/pages/index.html')


@login_required
def account(request):
    if request.method == 'GET':
        customer = Customer.objects.get(user=request.user)
        subscription = Subscription.objects.filter(customer=customer, is_active=True, paid=True)
        if not subscription.exists():
            return render(request, 'food_app/pages/account.html', context={'customer': customer})

        request_date = timezone.now()
        menus = []
        step_counter = 0
        steps_link = []
        calories_list = []
        while request_date < timezone.now() + timedelta(days=7):
            item = Menu.objects.filter(
                subscription=subscription.last(), date=request_date
            ).prefetch_related('recipe__ingredients')

            if not item.exists():
                break
            calories_list.append(item.aggregate(calories=Sum('recipe_id__calories')))
            menus.append(item)
            steps_link.append(step_counter)
            request_date += timedelta(days=1)
            step_counter += 1
        try:
            date_compare = timezone.now() + timedelta(days=int(request.GET.get('step', 0)))
        except ValueError:
            date_compare = timezone.now()
        calories = calories_list[int(request.GET.get("step", 0))]['calories']
        print()
        return render(
            request,
            'food_app/pages/account.html',
            context={
                'customer': customer,
                'subscription': subscription.last(),
                'menus': menus,
                'date_compare': date_compare.date(),
                'steps_link': steps_link,
                'calories': calories,
            },
        )

    elif request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.save()
        if request.FILES:
            customer = Customer.objects.get(user=request.user)
            customer.avatar = request.FILES['avatar']
            customer.save()

        messages.success(request, 'Данные успешно изменены.')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def order(request):
    if request.method == 'GET':
        order_form = OrderForm()
        return render(
            request,
            'food_app/pages/order.html',
            {
                'order_form': order_form,
            },
        )

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if not order_form.is_valid():
            return render(request, 'food_app/pages/order.html', {'order_form': order_form})

        price = order_form.cleaned_data['period'].price
        promocode = order_form.cleaned_data['promo_code']
        if promocode:
            price = price - price * promocode.discount / 100

        plan = Plan(
            price=price,
            period=order_form.cleaned_data['period'],
            recipe_category=order_form.cleaned_data['recipe_category'],
        )
        plan.save()
        plan.allergies.add(*order_form.cleaned_data['allergies'])
        plan.food_intakes.add(*order_form.cleaned_data['food_intakes'])
        plan.save()

        today = datetime.now()
        subscription_end = today + timedelta(mdays[today.month])

        subscription = Subscription(
            end=subscription_end,
            plan=plan,
            promocode=promocode if promocode else None,
        )

        subscription.save()
        customer = Customer.objects.get(user=request.user)
        customer.subscriptions.add(subscription)
        customer.save()

        return redirect('food_app:checkout')

    return redirect('food_app:order')


@login_required
def checkout(request):
    subscription = (
        Subscription.objects.filter(customer__user_id=request.user).order_by('-start').first()
    )
    price = subscription.plan.price
    discounted_price = (
        price - price * subscription.promocode.discount / 100 if subscription.promocode else None
    )

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)

        if not payment_form.is_valid():
            messages.warning(request, 'Исправьте ошибки в данных карты.')
            return render(
                request,
                'food_app/pages/checkout.html',
                {
                    'payment_form': payment_form,
                    'price': price,
                    'discounted_price': discounted_price,
                },
            )

        idempotence_key = str(uuid.uuid4())
        payment = Payment.create(
            {
                'amount': {
                    'value': discounted_price if discounted_price else price,
                    'currency': 'RUB',
                },
                'payment_method_data': {
                    'type': 'bank_card',
                    'card': {
                        'number': payment_form.cleaned_data['card_number'],
                        'expiry_year': f'20{payment_form.cleaned_data["card_year"]}',
                        'expiry_month': payment_form.cleaned_data['card_month'],
                        'csc': payment_form.cleaned_data["card_cvc"],
                        'cardholder': payment_form.cleaned_data['card_name'],
                    },
                },
                'confirmation': {
                    'type': 'redirect',
                    'return_url': request.build_absolute_uri(
                        reverse('food_app:payment_confirmation')
                    ),
                },
                'metadata': {},
                'capture': True,
                'description': 'Оплата: подписка на сервис FoodPlan',
                'test': True,
            },
            idempotence_key,
        )
        confirmation_url = payment.confirmation.confirmation_url
        request.session['payment_id'] = payment.id
        request.session['subscription_id'] = subscription.id
        return redirect(confirmation_url)

    price = subscription.plan.price
    discounted_price = (
        price - price * subscription.promocode.discount / 100 if subscription.promocode else None
    )
    payment_form = PaymentForm()

    return render(
        request,
        'food_app/pages/checkout.html',
        {
            'payment_form': payment_form,
            'price': price,
            'discounted_price': discounted_price,
        },
    )


@login_required
def payment_confirmation(request):
    payment_id = request.session.get('payment_id')
    subscription_id = request.session.get('subscription_id')

    request.session.pop('payment_id', None)
    request.session.pop('subscription_id', None)

    if not payment_id or not subscription_id:
        messages.error(request, 'Ошибка оплаты. Попробуйте, пожалуйста, снова.')
        return redirect('food_app:order')

    subscription = Subscription.objects.get(id=subscription_id)
    payment = Payment.find_one(payment_id)
    plan = subscription.plan

    if not subscription or not payment:
        messages.error(request, 'Ошибка оплаты. Попробуйте, пожалуйста, снова.')
        return redirect('food_app:order')

    if payment.status == 'succeeded':
        subscription.is_active = True
        subscription.paid = True
        subscription.save(update_fields=['is_active', 'paid'])

        messages.success(request, 'Подписка успешно оформлена!')
        return redirect('food_app:account')

    messages.error(request, 'Ошибка оплаты. Попробуйте, пожалуйста, снова.')
    plan = subscription.plan
    plan.delete()
    subscription.delete()
    return redirect('food_app:order')
