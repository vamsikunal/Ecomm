from django.shortcuts import render
from django.shortcuts import  redirect
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db.models import Q

import json
from .models import Order, Payment, OrderProduct
from store.models import Product
from cart.models import Cart, CartItem
# Create your views here.


def payment(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart = cart)
    order = Order.objects.filter(cart=cart, is_ordered=False).first()
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        payment = Payment(
            user = request.user,
            payment_id = body['transID'],
            payment_method = body['payment_method'],
            amount_paid = order.order_total,
            status = body['status'],
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        # Move the cart items to Orderd Product model
        cart = Cart.objects.get(user= request.user)
        cart_items = CartItem.objects.filter(cart = cart).all()

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # Clear cart
        cart_items.delete()

            # Send order recieved email to customer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('order_recieved_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        print("mail_done")
        # Send order number and transaction id back to sendData method via JsonResponse
        data = {
            'order_number': order.order_number,
            'transID': payment.payment_id,
        }
        return JsonResponse(data)
    context = {
        'cart_items' : cart_items,
        'cart':cart,
        'order':order, 
    }
    return render(request, 'payment.html', context)

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')



def order_list(request):
    orders = OrderProduct.objects.filter(user = request.user).all()
    context = {
        'orders':orders,
        'is_user_ordered': True,
    }
    return render(request, 'orders.html', context)


def search_orders(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = OrderProduct.objects.order_by('-created_date').filter(Q(OrderProduct__product_description__icontains = keyword) | Q(OrderProduct__product_name__icontains = keyword))
    context = {
        'products' : products
    }        
    return render(request, 'store.html', context)   
