from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# email messaging 
from django.core.mail import EmailMessage
from django.conf import settings
# email messaging done

# password reset modules 
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# password reset modules done

from .models import Profile
from .forms import SignupForm, ProfileForm, PasswordForm, RestPasswordForm
from cart.models import *


# Create your views here.
def account(request):
    return HttpResponse('Account Done')


def signout(request):
    logout(request)
    messages.success(request, 'Signout successful')
    return redirect('accounts:signin')


def signin(request):
    if request.method =="POST":
        name = request.POST['username']
        passw = request.POST['password']
        user = authenticate(username = name, password = passw)
        login(request, user)
        new = name.title()
        messages.success(request, f'Signin successful {new}!')
        return redirect('index')
    return render(request, 'signin.html')


def signup(request):
    regform = SignupForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        regform = SignupForm(request.POST)
        if regform.is_valid():
            newuser = regform.save()
            newprofile = Profile(user = newuser)
            newprofile.first_name = newuser.first_name
            newprofile.last_name = newuser.last_name
            newprofile.email = newuser.email
            newprofile.phone = phone
            newprofile.save()
            login(request, newuser)
            new = newuser.username.title()
            messages.success(request, f'Signup successful {new}!')
            return redirect('index')
        else:
            messages.error(request, regform.errors)
            return redirect('signup')
    return render(request, 'signup.html')

#authentication system done 


# user profile 
# @login_required(login_url='accounts:signin')
def profile(request):
    profile = Profile.objects.get(user__username = request.user.username)

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
        'profile':profile,
        'itemcount':itemcount,
    }
    return render(request, 'profile.html', context)


# @login_required(login_url='accounts:signin')
def profile_update(request):
    profile = Profile.objects.get(user__username = request.user.username)
    new = profile.user.username.title()
    # profile update 
    update = ProfileForm(instance=request.user.profile)#instatiate the profile update form for a GET request
    if request.method == 'POST':
        update = ProfileForm(request.POST, request.FILES,  instance=request.user.profile)#instatiate the profile update form for a POST request
        if update.is_valid():
            update.save()
            messages.success(request, f'Dear {new}, your profile update is successful!')
            return redirect('accounts:profile')
        else:
            messages.error(request, update.errors)
            return redirect('accounts:profile_update')

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
        'profile':profile,
        'update':update,
        'itemcount':itemcount,
    }
    return render(request, 'profile_update.html', context)




@login_required(login_url='accounts:signin')
def change_password(request):
    profile = Profile.objects.get(user__username = request.user.username)
    new = profile.user.username.title()
    form = PasswordForm(request.user)
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Dear {new}, your password change is successful.')
            return redirect('accounts:profile')
        else:
            messages.error(request, form.errors)
            return redirect('accounts:password')

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
        'profile':profile,
        'form':form,
        'itemcount':itemcount,
    }
    return render(request, 'password_change.html', context)
# user profile done

# password reset 
def password_reset_request(request):
	if request.method == "POST":
		reset_form = RestPasswordForm(request.POST)
		if reset_form.is_valid():
			data = reset_form.cleaned_data['email']
			users = User.objects.filter(Q(email=data))
			if users.exists():
				for user in users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					# 'domain':'54.175.228.118',
					'domain':'127.0.0.1:8000',
					'site_name': 'Avengers',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ('password_reset/done')

	reset_form = RestPasswordForm()

	return render(request=request, template_name="password/password_reset.html", context={
        "reset_form":reset_form
        })



