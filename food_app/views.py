from re import sub
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from yookassa import Payment

from calendar import mdays
from datetime import datetime, timedelta
import uuid

from food_app.forms import OrderForm, PaymentForm
from .models import Customer, Plan, Subscription


def index(request):
    return render(request, 'food_app/pages/index.html')


@login_required
def account(request):
    if request.method == 'GET':
        customer = Customer.objects.get(user=request.user)
        return render(request, 'food_app/pages/account.html', context={'customer': customer})
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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def order(request):
    if request.method == 'GET':
        order_form = OrderForm()
        return render(request, 'food_app/pages/order.html', {'order_form': order_form})

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if not order_form.is_valid():
            return render(request, 'food_app/pages/order.html', {'order_form': order_form})

        plan = Plan(
            price=1000,
            period=order_form.cleaned_data['period'],
            recipe_category=order_form.cleaned_data['recipe_categories'],
        )
        plan.save()
        plan.allergies.add(*order_form.cleaned_data['allergies'])
        plan.save()

        today = datetime.now()
        subscription_end = today + timedelta(mdays[today.month])

        subscription = Subscription(
            end=subscription_end,
            plan=plan,
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

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)

        if not payment_form.is_valid():
            return render(
                request,
                'food_app/pages/checkout.html',
                {
                    'payment_form': payment_form,
                    'price': subscription.plan.price,
                },
            )

        idempotence_key = str(uuid.uuid4())
        payment = Payment.create(
            {
                'amount': {'value': subscription.plan.price, 'currency': 'RUB'},
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

    payment_form = PaymentForm()
    return render(
        request,
        'food_app/pages/checkout.html',
        {
            'payment_form': payment_form,
            'price': subscription.plan.price,
        },
    )


@login_required
def payment_confirmation(request):
    payment_id = request.session.get('payment_id')
    subscription_id = request.session.get('subscription_id')

    request.session.pop('payment_id', None)
    request.session.pop('subscription_id', None)

    if not payment_id or not subscription_id:
        # TODO: add alert
        return redirect('food_app:order')

    subscription = Subscription.objects.get(id=subscription_id)
    payment = Payment.find_one(payment_id)

    if not subscription or not payment:
        # TODO: add alert
        return redirect('food_app:order')

    if payment.status == 'succeeded':
        # TODO: add alert
        subscription.is_active = True
        subscription.save()
        return redirect('food_app:account')

    # TODO: add alert
    plan = subscription.plan
    plan.delete()
    subscription.delete()
    return redirect('food_app:order')
