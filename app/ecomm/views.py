from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView, View, DetailView, FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from category.models import  Category
from store.models import Product
from cart.models import CartItem
# Create your views here.
class index(TemplateView):
    template_name = 'index.html'

class extra(TemplateView):
    template_name = 'ex.html'    


   