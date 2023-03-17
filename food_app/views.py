from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from calendar import mdays
from datetime import datetime, timedelta

from food_app.forms import OrderForm

from .models import Customer, Plan, Subscription


def index(request):
    return render(request, 'food_app/pages/index.html')


def order(request):
    return render(request, 'food_app/pages/order.html')


@login_required
def account(request):
    if request.method == 'GET':
        customer = Customer.objects.get(user=request.user)
        return render(
            request, 'food_app/pages/account.html',
            context={'customer': customer}
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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def order(request):
    if request.method == 'GET':
        order_form = OrderForm()
        return render(request, 'food_app/pages/order.html', {'order_form': order_form})

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if not order_form.is_valid():
            return render(request, 'food_app/pages/order.html', {'order_form': order_form})

        plan = Plan(
            price=5,
            period=order_form.cleaned_data['period'],
            recipe_category=order_form.cleaned_data['recipe_categories']
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

        return redirect(request, 'food_plan:index')



