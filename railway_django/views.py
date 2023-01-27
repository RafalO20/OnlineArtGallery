from email.mime import image
from http import client
from itertools import product
import logging
from multiprocessing import context
from os import stat
from pydoc import cli
# import razorpay
from threading import local
from xml.etree.ElementTree import QName
from django.http import JsonResponse
from django.shortcuts import redirect, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib import messages
from django.db.models import Q
from railway_django import settings


from railway_django.forms import CustomerProfileForm, CustomerRegistartionForm

from railway_django import models
# from .models import Cart, Customer

# from railway_django.forms import SignUpForm
 
# class SignUpView(CreateView):
#     form_class = SignUpForm
#     success_url = reverse_lazy('login')
#     template_name = 'commons/signup.html'

def about(request):
    return render(request, "about-us.html")

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
# from railway_django.forms import SignUpForm, ProfileForm
from django.contrib.auth.models import User

# Edit Profile View
# class ProfileView(UpdateView):
#     model = User
#     form_class = ProfileForm
#     success_url = reverse_lazy('home')
#     template_name = 'profile.html'


from .models import Cart, Customer, Order, OrderPlaced, Payment, Product
from django.views.generic import ListView, DetailView

class HomeView(ListView):
    model = Product
    template_name= "item_list.html"


def item_list(request):
    context = {
        'items': Product.objects.all()
    }
    return render(request, "item_list.html", context)

def arts_detail(request):
    context = {
        'items': Product.objects.all()
    }
    return render(request, "arts-detail.html", context)

def charge(request):
    return render(request, "charge.html")

from .models import Artists

def artists_list(request):
    context = {
        'artists': Artists.objects.all()
    }
    return render(request, "artists.html", context)

def order_summary(request):
    return render(request, "order-summary.html")

def card(request):
    return render(request, "card.html")

#CATEGORY

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"item_list.html",locals())

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,"arts-detail.html",locals())

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistartionForm()
        return render(request, 'signup.html', locals())
    def post(self,request):
        form = CustomerRegistartionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Gratulacje! Pomyślnie zarejestrowano użytkownika")
        else:
            messages.warning(request,"Nieprawidłowe dane")
        return render(request, 'signup.html', locals())

class ProfileView(View):
    def get(self, request):
            form = CustomerProfileForm()
            return render(request, 'profile.html', locals())
    def post(self, request):
            form = CustomerProfileForm(request.POST)
            if form.is_valid():
                user = request.user
                name = form.cleaned_data['name']
                locality = form.cleaned_data['locality']
                city = form.cleaned_data['city']
                mobile = form.cleaned_data['mobile']
                state = form.cleaned_data['state']
                zipcode = form.cleaned_data['zipcode']

                reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
                reg.save()
                messages.success(request, "Gratulację! Pomyślnie zapisano profil")
            else:
                messages.warning(request, "Nieprawidłowe dane")
            return render(request, 'profile.html', locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Gratulację! Profił zaktualizowany pomyślnie")
        else:
            messages.warning(request,"Nieprawidłowe dane")
        return redirect("address")

# def add_to_cart(request):
#     user=request.user
#     product_id = request.GET.get('prod_id')
#     if product_id.endswith('/'):
#         product_id = product_id[:-1]
#         logging.warning(product_id)
#     product = Product.objects.get(id=product_id)
#     Cart(user=user, product=product).save()
#     return redirect("/cart")

def add_to_cart(request):
    user = request.user
    test = Cart.objects.filter(user=user)
    product_id = request.GET.get('prod_id')
    # product_id = product_id[:-1]
    # if test:
    #     for t in test:
    #         if product_id == t.id:
    #             return
    if product_id.endswith('/'):
        product_id = product_id[:-1]
        logging.warning("fasfasf", product_id)
    if Cart.objects.filter(product=product_id).exists():
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 500
        print(prod_id)
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return redirect('/cart')
    else:
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/cart')
        
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40

    
    return render(request, 'add-to-cart.html',locals())


class checkout(View):
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['key'] = settings.STRIPE_PUBLISHABLE_KEY
    #     return context

    def get(self, request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
            totalamount = famount + 40
        #     razoramount = int(totalamount * 100)
        #     client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        #     data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        #     payment_response = client.order.create(data=data)
        #     print(payment_response)
        #     order_id = payment_response['id']
        #     order_status = payment_response['status']
        #     if order_status == 'created':
        #         payment = Payment(
        #             user=user,
        #             amount=totalamount,
        #             razorpay_order_id=order_id,
        #             razorpay_payment_status = order_status
        #         )
        #         payment.save()
        return render(request, 'checkout.html',locals())

# def charge(request):
#     if request.method == 'POST':
#         charge = stripe.Charge.create(
#                 amount = 500,
#                 currency="zł",
#                 description = '"A Django charge',
#                 source=request.POST['stripeToken']
#         )
#         return render(request, 'charge.html')
    
    



# def payment_done(request):
#     order_id = request.GET.get('order_id')
#     payment_id=request.GET.get('payment_id')
#     cust_id=request.GET.get('cust_id')
#     user=request.user
#     customer=Customer.objects.get(id=cust_id)
#     payment=Payment.objects.get(razorpay_order_id=order_id)
#     payment.paid = True
#     payment.razorpay_payment_id = payment_id
#     payment.save()
#     cart = Cart.objects.filter(user=user)
#     for c in cart:
#         OrderPlaced(user=user,customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
#         c.delete()


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove(request):
    Cart.objects.all().delete()
    return render(request, 'remove.html',locals())


