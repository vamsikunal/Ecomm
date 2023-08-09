from .models import Cart, CartItem

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                cart = Cart.objects.filter(user = request.user).first()
                cart_items = CartItem.objects.filter(cart = cart)
                for cart_item in cart_items:
                    cart_count += 1
            else:
                cart_count = 0         
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)                    