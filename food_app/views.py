from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Customer


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
