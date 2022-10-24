from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from mainapp.models import Product

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True, blank=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	device = models.CharField(max_length=36, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
    

	def __str__(self):
		if self.name:
			name = self.name
		else:
			name = str(self.device)
		return name



class Order(models.Model):
	customer = models.OneToOneField(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	complete = models.BooleanField(default=False)
	transaction_code = models.CharField(max_length=10, null=True, blank=True)
	payment_code = models.CharField(max_length=36, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order_item = models.IntegerField(default=1)
	price = models.IntegerField(null=True, blank=True)
	quantity = models.IntegerField(null=True, blank=True)
	amount = models.FloatField(null=True, blank=True)
	order_code = models.CharField(max_length=10, null=True, blank=True)
	complete = models.BooleanField(default=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product.p_name
	


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    total = models.IntegerField()
    order_code = models.CharField(max_length=255)
    pay_code = models.CharField(max_length=36)
    phone = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    pay_date = models.DateTimeField(auto_now_add=True)
    admin_note = models.CharField(max_length=255)
    admin_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.user.username

    class Meta:
        db_table = 'payment'
        managed = True
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
   


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	order_code = models.CharField(max_length=255)
	first_name = models.CharField(max_length=50, default='a')
	last_name = models.CharField(max_length=50, default='a')
	phone = models.CharField(max_length=200, null=False)
	address = models.CharField(max_length=200,blank=True, null=True)
	city = models.CharField(max_length=200, blank=True, null=True)
	state = models.CharField(max_length=200, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address