# Create your views here.
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime

# from django.shortcuts import render,HttpResponse,redirect
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.decorators import login_required

# @login_required(login_url='login')
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products,'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

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

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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
                    zipcode=data['shipping']['zipcode']
                )

        else:
            print('User is not logged in..')

    return JsonResponse('Payment complete!', safe=False)


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('store:store_page')  # Adjust 'store_page' according to your URL pattern
    else:
        form = SignUpForm()
    return render(request, 'store/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store:store_page')  # Adjust 'store_page' according to your URL pattern
        else:
            return render(request, 'store/login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'store/login.html')



# def SignupPage(request):
#     if request.method == 'POST':
#         uname = request.POST.get('username')
#         email = request.POST.get('email')
#         pass1 = request.POST.get('password1')
#         pass2 = request.POST.get('password2')
#
#         if pass1 != pass2:
#             return HttpResponse("Your password and confrom password are not Same!!")
#         else:
#
#             my_user = User.objects.create_user(uname, email, pass1)
#             my_user.save()
#             return redirect('login')
#
#     return render(request, 'signup.html')
#
#
# def LoginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         pass1 = request.POST.get('pass')
#         user = authenticate(request, username=username, password=pass1)
#         if user is not None:
#             login(request, user)
#             return redirect('store')
#         else:
#             return HttpResponse("Username or Password is incorrect!!!")
#
#     return render(request, 'login.html')
#
#
# def LogoutPage(request):
#     logout(request)
#     return redirect('login')

