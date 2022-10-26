from zoneinfo import available_timezones
from django.shortcuts import render, HttpResponse

from mainapp.models import Category,Product
from cart.models import *
# Create your views here.

def index(request):
    categories = Category.objects.all().order_by('-id')[:4]

    context = {
        'categories':categories,
    }
    return render(request, 'index.html', context)


def products(request):
    products = Product.objects.all().order_by('-id')
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
        'products':products,
        'itemcount':itemcount,
    }
    return render(request, 'products.html', context)


def categories(request):
    categories = Category.objects.all()
    
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
        'categories':categories,
        'itemcount':itemcount,
    }
    return render(request, 'categories.html', context)


def category(request, id, slug):
    single_category = Product.objects.filter(category_id=id)

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
        'single_category':single_category,
        'itemcount':itemcount,
    }
    return render(request, 'category.html', context)


def product_details(request, id, slug):
    details = Product.objects.get(pk=id)

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
        'details':details,
        'itemcount':itemcount,
    }
    return render(request, 'details.html', context)
