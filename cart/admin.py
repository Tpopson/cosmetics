from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user','name','email','device','date_created']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','complete','transaction_code','payment_code','date_ordered']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order','order_item','price','quantity','amount','order_code','complete', 'date_added')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','customer','first_name','last_name','phone','total','order_code','pay_code','paid','pay_date','admin_note','admin_update')
    readonly_fields = ('customer','first_name','last_name','phone','total','order_code','pay_code','paid','pay_date')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order','order_code','first_name','last_name', 'phone', 'address', 'city', 'state', 'date_created')