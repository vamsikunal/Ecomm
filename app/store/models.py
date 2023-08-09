from django.db import models
from django.urls import reverse

from category.models import Category
from accounts.models import Account
from cart.models import WishlistItem, Wishlist
from django.conf import settings


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    product_description = models.TextField(blank=True)
    orignal_price = models.IntegerField(null=True)
    price = models.IntegerField()
    product_image = models.ImageField(upload_to='product')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('store:product_detail', args = [self.category.slug, self.slug])

    @property
    def percentage_off(self):
        return int((self.price)/self.orignal_price*100)

    @property
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self)
        count = 0
        for review in reviews.all():
            count = count + review.rating
        if count == 0:
            return 1.0   
        return round(count/reviews.count(),1)

    @property
    def product_exist_in_wishlist(self):
        if WishlistItem.objects.filter(product = self).exists():
            return True
        else:
            return False   




class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.IntegerField(blank=False)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self. created_at.strftime("%B")
   

