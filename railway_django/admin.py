from django.contrib import admin

from .models import Cart, Customer, OrderPlaced, Payment, Product, Artists

# admin.site.register(Item)
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'product_image','discounted_price']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']

@admin.register(Cart)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product','quantity']
# admin.site.register(OrderItem)
# admin.site.register(Order)
admin.site.register(Artists)


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity', 'ordered_date', 'status', 'payment']