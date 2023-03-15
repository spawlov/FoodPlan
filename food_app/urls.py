from django.urls import path

from food_app import views

app_name = 'food_app'

urlpatterns = [
    path('', views.index, name='index'),
]
