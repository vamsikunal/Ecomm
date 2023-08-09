from django.db import models
from accounts.models import Account
# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, null=True)
    cart_price  = models.IntegerField(default=0)
    tax_persent = 18 
    
    @property
    def tax(self):
        return (self.cart_price*self.tax_persent)/100

    @property
    def total_price(self):
        return self.cart_price + (self.cart_price*self.tax_persent)/100

    def __str__(self):
        return self.user.username

class  CartItem(models.Model):
    product = models.ForeignKey(to="store.Product", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
       return self.product.price * self.quantity 


class Wishlist(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

class WishlistItem(models.Model):
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    wishlist =  models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.wishlist.user.username

   




