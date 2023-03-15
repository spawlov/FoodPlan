from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'food_app/pages/index.html')

def order(request):
    return render(request, 'food_app/pages/order.html')

def account(request):
    return render(request, 'food_app/pages/account.html')
