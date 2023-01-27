"""railway_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ast import pattern
from base64 import urlsafe_b64decode
from ipaddress import summarize_address_range
from re import template
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from railway_django.forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from railway_django.views import CreateView, item_list
from .views import artists_list, item_list, charge
from . import views

# arts_detail, add_to_cart, payment_done, orders
urlpatterns = [
    path('admin/', admin.site.urls),
    path('about-us/', views.about,name="about-us"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='homepage.html'), name='home'),
    path('item_list/<slug:val>', views.CategoryView.as_view(), name="item_list"),
    path('arts-detail/<int:pk>', views.ProductDetail.as_view(), name="arts-detail"),
    path('artists/', artists_list, name='artists_list'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name="updateAddress"),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    # path('paymentdone/', views.payment_done, name="paymentdone"),
    # path('orders/', views.orders, name='orders'),

    # path('payments/', include('payments.urls')),

    path('charge/', views.charge, name='charge'),
    path('remove/', views.remove, name='remove'),
    

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    # path('checkout/', checkout, name='checkout'),
    path('order-summary/', views.order_summary, name='order-summary'),
    path('card/', views.card, name="card"),
    # path('product/<slug>', ItemDetailView.as_view(), name='product'),
    # path('add-to-cart/<slug>', add_to_cart, name="add-to-cart"),
    # path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),


    #login authentication
    path('signup/', views.CustomerRegistrationView.as_view(), name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('password-reset/', auth_views.PasswordResetView.as_view (template_name="password-reset.html", form_class=MyPasswordResetForm), name='password-reset'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password-reset.html')),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='password-reset-done.html'), name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password-reset-confirm.html',form_class=MySetPasswordForm), name='password-reset-confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password-reset-complete.html'), name='password-reset-complete'),
    path('item_list/', item_list, name='item_list'),
    # path('arts-detail/', arts_detail, name='arts-detail'),
    path('artists/', artists_list, name='artists_list'),
    # path('add-to-cart/', add_to, name='add-to-cart'),
]  

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)