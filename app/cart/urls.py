from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('add_wish_detail/<int:product_id>/', views.add_wishlist_detail, name='add_wishlist_detail'),
    path('add_wish_store/<int:product_id>/', views.add_wishlist_store, name='add_wishlist_store'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('new_address/', views.new_address, name='new_address'),
    path('remove_wishlist_store/<int:product_id>/', views.remove_wishlist_store, name='remove_wishlist_store'),
    path('remove_wishlist_detail/<int:product_id>/', views.remove_wishlist_detail, name='remove_wishlist_detail'),
]