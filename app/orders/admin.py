from django.contrib import admin
from .models import OrderProduct, Order, Payment
# Register your models here.


admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)