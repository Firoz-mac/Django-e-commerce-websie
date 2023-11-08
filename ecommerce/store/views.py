from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from ecommerce import settings
from django.core.mail import send_mail

def store(request):

    data = cookieCart(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    img = CarousalImg.objects.all()
    context={'products':products, 'cartItems':cartItems, 'img':img}
    return render(request, 'store/store.html',context)

def cart(request):

    data = cookieCart(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
            

    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html',context)




def checkout(request):
    
    data = cookieCart(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['Action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)


    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()



    return JsonResponse('item was added', safe=False)

#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id


    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )


    return JsonResponse('payment complete!', safe=False)


def login(request):    
        
    return render(request, 'store/login.html')

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist try another one")
            return render(request, 'store/signup.html')
        if User.objects.filter(email=email):
             messages.error(request, "Email already exist try another one")
             return render(request, 'store/signup.html')
        if len(username)>10:
            messages.error(request, "Username Must be under 10 characters")
        if pass1 != pass2:
            messages.error(request, "Passwords didnt match")
        if not username.isalnum():
            messages.error(request, "Username must be alpha numeric")
            return render(request, 'store/signup.html')
            

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account have been Successfully Created.")

        #welcome email

        subject = "welcome to shopper"
        message = "Hello" + myuser.first_name + "!! \n" + "welcome to shopper \n Thank you for visiting our website \n we have also send a confirmation email please confirm your email address to activate your account. \n Thank You \n Happy Shopping"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return render(request, 'store/signin.html')




    return render(request, 'store/signup.html')

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']


        user = authenticate(username=username, password=pass1)


        if user is not None:
            login(request)
            #fname = user.username
            return render(request, 'store/welocme.html')
        else:
            messages.error(request, "Bad Credentials")
            return render(request, 'store/signup.html')


    return render(request, 'store/signin.html')

def welcome(request):
    return render(request, 'store/welocme.html')
def contact(request):
    return render(request, 'store/contact.html')

def offeritems(request):
    data = cookieCart(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    img = CarousalImg.objects.all()
    context={'products':products, 'cartItems':cartItems, 'img':img}
    return render(request, 'store/offeritems.html',context)

def trending(request):
    data = cookieCart(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    img = CarousalImg.objects.all()
    context={'products':products, 'cartItems':cartItems, 'img':img}
    return render(request, 'store/trending.html',context)

def futureditems(request):
    data = cookieCart(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    img = CarousalImg.objects.all()
    context={'products':products, 'cartItems':cartItems, 'img':img}
    return render(request, 'store/futureditems.html',context)
