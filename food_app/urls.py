from django.conf.locale import vi
from django.urls import path

from food_app import views

app_name = 'food_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('order/', views.order, name='order'),
    path('account/', views.account, name='account'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment_confirmation/', views.payment_confirmation, name='payment_confirmation'),
    path('get_plan_price/', views.get_plan_price, name='get_plan_price'),
]
