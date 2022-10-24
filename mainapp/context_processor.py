from django.contrib.auth.models import User
from .models import Category
from cart.models import OrderItem, Customer, Order


def catedropdown(request):
    categories = Category.objects.all()

    context ={
        'categories':categories
    }

    return context




def cartcount(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem = OrderItem.objects.filter(order=order, complete=False)

    itemcount = 0

    for item in orderitem:
        itemcount += item.order_item


    context = {
        'itemcount': itemcount
    }

    return context
