from store.models import Product
from .models import Cart, CartItem, Wishlist, WishlistItem
from accounts.models import Address
from accounts.forms import AddressForm
from orders.models import Order
from django.http import HttpResponse
from django.shortcuts import  redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.sites.shortcuts import  get_current_site
from django.shortcuts import  render
from django.urls import reverse
# Create your views here.


def _cart_id(request):
    cart_session = request.session.session_key
    if not cart_session:
        cart_session = request.session.create()
    return cart_session   

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated: 
        cart = Cart.objects.filter(user=request.user).first()
    else:    
        return redirect('cart')
    
    try:
        cart_item = CartItem.objects.get(product = product, cart = cart)
        if cart_item.product.stock > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, 'Sorry for the inconvenience but the product ' + cart_item.product.product_name + ' has this much stock available')    
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product = product, cart = cart, quantity = 1)
    item_exist_in_wishlist = WishlistItem.objects.filter(product=product).exists()
    if item_exist_in_wishlist:
        print('hello')
        WishlistItem.objects.filter(product=product).delete()
        cart_item.save()

    return redirect('cart')

def add_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist = Wishlist.objects.filter(user=request.user).first()
    is_item_exist = WishlistItem.objects.filter(wishlist = wishlist, product=product).exists()
    if not is_item_exist:
        wishlist_item = WishlistItem.objects.create(wishlist = wishlist, product=product)
        wishlist_item.save()


def add_wishlist_store(request, product_id):
    if request.user.is_authenticated:
        add_wishlist(request, product_id)
    else:
        return redirect('cart')
    return redirect('/store')

def add_wishlist_detail(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        add_wishlist(request, product_id)
    else:
        return redirect('cart')
    return HttpResponseRedirect(reverse('store:product_detail', args = [product.category.slug, product.slug]))

def remove_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist = Wishlist.objects.filter(user=request.user).first()
    wishlist_item = WishlistItem.objects.get(wishlist = wishlist, product=product)
    wishlist_item.delete()

def remove_wishlist_store(request, product_id):
    remove_wishlist(request, product_id)
    return redirect('/store')

def remove_wishlist_detail(request, product_id):
    remove_wishlist(request, product_id)
    product = Product.objects.get(id=product_id)
    return HttpResponseRedirect(reverse('store:product_detail', args = [product.category.slug, product.slug]))


def remove_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.filter(user= request.user).first()
    cart_item = CartItem.objects.get(product = product, cart = cart)
    cart_item.quantity =  cart_item.quantity - 1
    cart_item.save()
    if(cart_item.quantity == 0):
        cart_item.delete()
        return redirect('cart') 
    return redirect('cart') 

def remove_cart_item(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    cart = Cart.objects.get(user= request.user)
    cart_item = CartItem.objects.get(product = product, cart = cart)
    cart_item.delete()
    return redirect('cart') 

def cart(request, total_price=0, cart_items=None):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_items = CartItem.objects.filter(cart = cart)
        wishlist = Wishlist.objects.filter(user=request.user).first()
        wishlist_items = WishlistItem.objects.filter(wishlist = wishlist)        
        for cart_item in cart_items:
            total_price += (cart_item.product.price * cart_item.quantity)
        cart.cart_price = total_price
        cart.save()
        try:
            order = Order.objects.filter(user=request.user, is_ordered=False).all()
            order.delete()
        except AttributeError:
            pass

    else:    
        messages.info(request, 'Login to see the items you added in cart')
        return redirect('login')

    context = {
        'cart_items' : cart_items,
        'cart':cart,
        'wishlist_items':wishlist_items,
    }

    return render (request, 'cart.html', context)        



def checkout(request, cart_items=None):
    flag = False
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart = cart)
    saved_address = Address.objects.filter(user=request.user).all()
    order = Order.objects.filter(cart=cart).first()
    if request.method == 'POST':
        if request.POST.get('address'):
            address = Address.objects.filter(pk=request.POST.get('address')).first()
            user = request.user
            ip = request.META.get('REMOTE_ADDR')
            order = Order.objects.create(address=address, user=user, order_total=cart.total_price, tax=cart.tax, ip=ip, cart=cart)
            order.generate_order_number()
            order.save()
            flag = True
            address_form = None
            return redirect('payment')
        else:
            pass 
    else:
        address_form = AddressForm()

    context = {
        'cart_items' : cart_items,
        'cart':cart,
        'saved_address':saved_address,
        'flag':flag,
        'order':order,
        'address_form':address_form,
        
    }
    return render(request, 'checkout.html', context) 


def new_address(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address =  address_form.save(commit=False)
            address.user = request.user
            address.locality = address_form.cleaned_data['locality']
            address.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)



