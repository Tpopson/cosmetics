from zoneinfo import available_timezones
from django.shortcuts import render, HttpResponse

from mainapp.models import Category,Product
# Create your views here.

def index(request):
    categories = Category.objects.all().order_by('-id')[:4]

    context = {
        'categories':categories
    }
    return render(request, 'index.html', context)


def products(request):
    products = Product.objects.all().order_by('-id')
   
    context = {
        'products':products,
    }
    return render(request, 'products.html', context)


def categories(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }
    return render(request, 'categories.html', context)


def category(request, id, slug):
    single_category = Product.objects.filter(category_id=id)
                          
    context = {
        'single_category':single_category
    }
    return render(request, 'category.html', context)


def product_details(request, id, slug):
    details = Product.objects.get(pk=id)

    context = {
        'details':details
    }
    return render(request, 'details.html', context)
