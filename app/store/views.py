from django.shortcuts import redirect, render
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView, View, DetailView, FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from orders.models import OrderProduct
from cart.models import  WishlistItem
from category.models import  Category
from store.models import Product, ReviewRating
from cart.models import  CartItem, Cart

# Create your views here.



def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category,  slug =  category_slug)
        products = Product.objects.filter(category = categories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_products = paginator.get_page(page_number)
        product_count = products.count()

    context = {
        'products' : page_products,
        'product_count' : product_count,
    }


    return render(request, 'store.html', context)    


def product_detail(request, category_slug, product_slug):
    # __ to get access of slug of category model
    single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
    is_user_ordered = OrderProduct.objects.filter(product = single_product, user= request.user).exists()
    count = ReviewRating.objects.filter(product = single_product).count()
    print(is_user_ordered)
    ratings = ReviewRating.objects.filter(product = single_product)
    product_exist_in_wishlist = WishlistItem.objects.filter(product = single_product).exists()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user).first()
        in_cart = CartItem.objects.filter(cart = cart, product = single_product).exists()
    else:    
        in_cart = False
    context = {
         'single_product' : single_product,
         'in_cart' : in_cart,
         'product_exist_in_wishlist':product_exist_in_wishlist,
         'ratings':ratings,
         'is_user_ordered':is_user_ordered,
         'count':count
    }
    return render(request, 'product-detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_description__icontains = keyword) | Q(product_name__icontains = keyword) | Q(category__category_name__icontains = keyword))
    context = {
        'products' : products
    }        
    return render(request, 'store.html', context)    


def review(request, category_slug, product_slug):
    print(product_slug)
    single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        subject = request.POST.get('subject')
        print(type(rating))
        ReviewRating.objects.create(rating = rating, review = review, subject = subject, user= request.user, ip = request.META.get('REMOTE_ADDR'), product=single_product)
        return redirect(single_product.get_url())
    return render(request, 'review_form.html')    