from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'food_app/pages/index.html')


def order(request):
    return render(request, 'food_app/pages/order.html')


@login_required
def account(request):
    if request.method == 'GET':
        user = User.objects.get(pk=request.user.id)
        print(user)
        return render(request, 'food_app/pages/account.html')
    return render(request, 'food_app/pages/account.html')
