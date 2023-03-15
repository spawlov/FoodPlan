from django.conf.locale import vi
from django.urls import path

from food_app import views

app_name = 'food_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('order/', views.order, name='order'),
    path('account/', views.account, name='account'),
]
