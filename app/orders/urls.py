from django.urls import path
from . import views

urlpatterns = [
    path('order_complete/', views.order_complete, name='order_complete'),
    path('payment/', views.payment, name='payment'),
    path('order_list', views.order_list, name='order_list'),
]