import random
import string
import requests
import json


from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages

from accounts.views import profile

from . models import *
from mainapp.models import Product
from accounts.models import Profile
from accounts.forms import SignupForm

# Create your views here.
def index(request):
    return HttpResponse('cart ap done')


def addtocart(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        prod = request.POST['prodid']
        prodid = Product.objects.get(pk=prod)
        try:
            customer = request.user.customer	
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=prodid)
            orderItem.quantity= quantity
            orderItem.price = prodid.p_price
            orderItem.amount=prodid.p_price * quantity
            orderItem.save()
            messages.success(request, 'Your order is being proccessed!')
        return redirect(url)
    return redirect(url)




def mycart(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem = OrderItem.objects.filter(order=order, complete=False)
    
    subtotal = 0
    vat = 0
    total = 0

    for item in orderitem:
        subtotal += item.amount

    #7.5% of subtotal
    vat = 0.075 * subtotal 

    total = vat + subtotal

    context = {
        'customer':customer,
        'orderitem':orderitem,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
    }
    return render(request, 'cart.html', context)


def deleteitem(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitem  = OrderItem.objects.filter(order=order, complete=False)

        anitem = request.POST['dishid']
        deletedish = OrderItem.objects.filter(pk=anitem)
        deletedish.delete()
        messages.success(request, 'Order item deleted successfully.')
    return redirect(url)


def deletecart(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitem = OrderItem.objects.filter(order=order, complete=False)

        deleteall = OrderItem.objects.filter(order = order, complete=False)
        deleteall.delete()
        messages.success(request, 'You have deleted all the items in your shopcart.')
    return redirect(url)


#decrease cart item quantity
def decrease(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitem = OrderItem.objects.filter(order=order, complete=False)

        itemquantity = int(request.POST['decrease'])
        cartitem = request.POST['itemid']
        decreasecart = OrderItem.objects.get(pk= cartitem)
        decreasecart.quantity -= itemquantity
        decreasecart.amount = decreasecart.price * decreasecart.quantity
        decreasecart.save()
        messages.success(request, 'Quantity decreased.')
    return redirect(url)


#increase cart item quantity
def increase(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitem = OrderItem.objects.filter(order=order, complete=False)

        itemquantity = int(request.POST['increase'])
        cartitem = request.POST['itemid']
        increasecart = OrderItem.objects.get(pk=cartitem)
        increasecart.quantity += itemquantity
        increasecart.amount = increasecart.price * increasecart.quantity
        increasecart.save()
        messages.success(request, 'Quantity increased.')
    return redirect(url)



def placeorder(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer = Customer.objects.get(device=device)

    regform = SignupForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        regform = SignupForm(request.POST)
        if regform.is_valid():
            newuser = regform.save()
            newprofile = Profile(user = newuser)
            newprofile.first_name = newuser.first_name
            newprofile.last_name = newuser.last_name
            newprofile.email = newuser.email
            newprofile.phone = phone
            newprofile.address = address
            newprofile.city = city
            newprofile.state = state
            newprofile.save()
            login(request, newuser)
            new = newuser.first_name.title()
            messages.success(request, f'Dear {new} your order is being processed, kindly proceed to make payment. Thank you!')
            return redirect('cart:checkout')
        else:
            messages.error(request, regform.errors)
        return redirect('cart:mycart')




def checkout(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem  = OrderItem.objects.filter(order=order, complete=False)
    profile = Profile.objects.get(user__username = request.user.username)

    subtotal = 0
    vat = 0
    total = 0

    for item in orderitem:
        subtotal += item.amount

    #7.5% of subtotal
    vat = 0.075 * subtotal 

    total = vat + subtotal


    context = {
        'orderitem':orderitem,
        'profile':profile,
        'total':total,
    }
    return render(request, 'checkout.html', context)



def payment(request):
    url = request.META.get('HTTP_REFERER')
    
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    if request.method == 'POST':
        api_key = 'sk_test_0c3bb25f14513ee95dcbe057e8b007f8b8480aa1'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://54.175.228.118/cartcallback'
        # cburl = 'http://localhost:8000/cartcallback'
        ref_code = ''.join(random.choices(string.digits + string.ascii_letters, k=8))
        user = User.objects.get(username = request.user.username)
        email = user.email
        ccode = Customer.objects.get(device=customer)
        cart_code = ccode.device
        theorder = Order.objects.get(customer=ccode)
        total = float(request.POST['total']) * 100
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        phone = request.POST['phone']
        new_email = request.POST['email']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']

        headers = {'Authorization': f'Bearer {api_key}'}#pass in the test key
        data = {'reference': ref_code, 'amount': int(total), 'order_number': cart_code, 'email': email, 'callback_url':cburl, 'currency': 'NGN'}

        try: #make call to Paystack
            r = requests.post(curl, headers=headers, json=data)#pip install requests
        except Exception:
            messages.error(request, 'Network busy, refresh and try again.')
        else:
            transback = json.loads(r.text)#import json, import requests
            rurl = transback['data']['authorization_url']

            account = Payment()
            account.customer = ccode
            account.first_name = fname
            account.last_name = lname
            account.phone = phone
            account.total = total/100
            account.order_code = cart_code
            account.pay_code = ref_code
            account.paid = True
            account.save()

            ship = ShippingAddress()
            ship.customer = ccode
            ship.order = theorder
            ship.order_code = cart_code
            ship.phone = phone
            ship.first_name = fname
            ship.last_name = lname
            ship.address = address
            ship.city = city
            ship.state = state
            ship.save() 

            email = EmailMessage(
                'Order confirmation',#message Title
                f'Dear {fname}, your order is confirmed! \n Your delivery is in one hour. \n Thank you for your patronage.',#content
                settings.EMAIL_HOST_USER, #compay email
                [new_email]#client email
                )
            
            email.fail_silently = True
            email.send()

            return redirect(rurl)
    return redirect(url)


def callback(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    profile = Profile.objects.get(user__username = request.user.username)
    cart = OrderItem.objects.filter(order = order, complete= False)
    
    for item in cart:
        item.complete = True
        item.order_code = customer.device
        item.save()

        stock = Product.objects.get(pk = item.product.id)
        stock.p_max -= item.quantity
        stock.save()

    context = {
        'profile':profile
        }
    return render(request, 'callback.html', context)