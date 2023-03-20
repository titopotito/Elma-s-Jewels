from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Jewelry, CartItem, Cart, Address, ContactDetail
from django.contrib.auth.models import User
from .forms import CreateUserForm, CreateAddressForm, CreatePhoneNumberForm


def index(request):
    if request.method == 'GET':
        best_sellers = Jewelry.objects.all().order_by('-sold')[:6]
        context = {'best_sellers': best_sellers}
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user.id)
            cart_item_count = CartItem.objects.filter(cart=cart.id).count()
            context['cart'] = cart
            context['cart_item_count'] = cart_item_count

        return render(request, 'index.html', context)


@login_required(login_url='login')
def profile(request):
    if request.method == 'GET':
        cart = Cart.objects.get(user=request.user.id)
        cart_item_count = CartItem.objects.filter(cart=cart.id).count()
        address = Address.objects.get(user=request.user.id)
        context = {
            'cart': cart,
            'cart_item_count': cart_item_count,
            'address': address
        }

        return render(request, 'profile.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# CART ///////////////////////////////////////////////////////////
@login_required(login_url='login')
def cart_page(request):
    if request.method == 'GET':
        cart = Cart.objects.get(user=request.user.id)
        cart_items = CartItem.objects.filter(cart=cart.id).order_by('id')
        cart_item_count = cart_items.count()

        total_cost = 0
        if cart_items.count() > 0:
            for cart_item in cart_items:
                total_cost = total_cost + (cart_item.sub_total*cart_item.order_quantity)

        context = {
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
            'cart': cart,
            'total_cost': total_cost
        }
        return render(request, 'cart.html', context)


@login_required(login_url='login')
def add_cart_item(request, jewelry_id):
    if request.method == 'POST':
        jewelry = Jewelry.objects.get(pk=jewelry_id)
        cart = Cart.objects.get(user=request.user.id)
        cart_item = CartItem(cart=cart, jewelry=jewelry, order_quantity=1, sub_total=jewelry.price)
        cart_item.save()
        return redirect('cart')


@login_required(login_url='login')
def delete_cart_item(request, cart_item_id):
    if request.method == 'POST':
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        return redirect('cart')


@login_required(login_url='login')
def update_cart_item(request, cart_item_id):
    if request.method == 'POST':
        if int(request.POST['order-quantity']) == 0:
            delete_cart_item(request, cart_item_id)
            return redirect('cart')
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.order_quantity = request.POST['order-quantity']
        cart_item.save()
        return redirect('cart')

# SHOP /////////////////////////////////////////////////////////////////////////////////


def shop_page(request):
    if request.method == 'GET':
        jewelry = Jewelry.objects.all().order_by('-sold')

        (filtered_jewelry, category_options, metal_options, stone_options) = filter_jewelry(request, jewelry)
        (sorted_jewelry, sort_option) = sort_jewelry(request, filtered_jewelry)

        paginator = Paginator(sorted_jewelry, 16)
        page = request.GET.get('page')
        paged_jewelry = paginator.get_page(page)

        context = {
            'jewelry': paged_jewelry,
            'sort_option': sort_option,
            'category_options': category_options,
            'metal_options': metal_options,
            'stone_options': stone_options
        }

        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user.id)
            cart_item_count = CartItem.objects.filter(cart=cart.id).count()
            context['cart'] = cart
            context['cart_item_count'] = cart_item_count

        return render(request, 'shop.html', context)


def filter_jewelry(request, jewelry):
    if request.method == 'GET':
        category_options = []
        metal_options = []
        stone_options = []
        if 'category' in request.GET:
            category_options = request.GET.getlist('category')
            jewelry = jewelry.filter(category__in=category_options)
        if 'metal' in request.GET:
            metal_options = request.GET.getlist('metal')
            jewelry = jewelry.filter(metal__overlap=metal_options)
        if 'stone' in request.GET:
            stone_options = request.GET.getlist('stone')
            jewelry = jewelry.filter(stone__overlap=stone_options)
        return (jewelry, category_options, metal_options, stone_options)


def sort_jewelry(request, jewelry):
    if request.method == 'GET':
        sorted_jewelry = jewelry.order_by('-sold')
        sort_option = 'best-selling'
        if 'sort-option' in request.GET:
            sort_option = request.GET['sort-option']
            if sort_option == 'best-selling':
                return (sorted_jewelry, sort_option)
            elif sort_option == 'a-z':
                sorted_jewelry = jewelry.order_by('name')
            elif sort_option == 'z-a':
                sorted_jewelry = jewelry.order_by('-name')
            elif sort_option == 'low-high':
                sorted_jewelry = jewelry.order_by('price')
            elif sort_option == 'high-low':
                sorted_jewelry = jewelry.order_by('-price')
            elif sort_option == 'old-new':
                sorted_jewelry = jewelry.order_by('date_added')
            elif sort_option == 'new-old':
                return jewelry.order_by('-date_added')
        return (sorted_jewelry, sort_option)


def jewelry_page(request, jewelry_id):
    if request.method == 'GET':
        jewelry = Jewelry.objects.get(pk=jewelry_id)
        context = {'jewelry': jewelry}

        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user.id)
            cart_item_count = CartItem.objects.filter(cart=cart.id).count()
            context['cart'] = cart
            context['cart_item_count'] = cart_item_count

        return render(request, 'jewelry.html', context)


# PAYMENT ////////////////////////////////
@login_required(login_url='login')
def checkout(request):

    if request.method == 'GET':
        checkout_item_ids = request.GET.getlist('checkout-item-ids')
        checkout_items = CartItem.objects.filter(id__in=checkout_item_ids)
        address = Address.objects.get(user=request.user.id)
        phone_number = ContactDetail.objects.get(user=request.user.id).phone_number

        total_cost = 0
        if checkout_items.count() > 0:
            for checkout_item in checkout_items:
                total_cost = total_cost + (checkout_item.sub_total*checkout_item.order_quantity)

        context = {
            'checkout_items': checkout_items,
            'total_cost': total_cost,
            'address': address,
            'phone_number': phone_number
        }

        return render(request, 'checkout.html', context)


def shipping(request):
    return render(request, 'shipping.html')

###############################################


def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or Password is not correct.')

    context = {
        'cart_item_count': CartItem.objects.all().count(),
        'messages': messages
    }
    return render(request, 'login.html', context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = CreateUserForm()
    form2 = CreateAddressForm()
    form3 = CreatePhoneNumberForm(request.POST)

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form2 = CreateAddressForm(request.POST)
        form3 = CreatePhoneNumberForm(request.POST)
        for field in form:
            print("Field Error:", field.name,  field.errors)

        if form.is_valid():
            if form2.is_valid():
                if form3.is_valid():
                    new_user = form.save()
                    user = User.objects.get(pk=new_user.id)
                    address = form2.save(commit=False)
                    address.user = user
                    address.save()
                    phone_number = form3.save(commit=False)
                    phone_number.user = user
                    phone_number.save()
                    cart = Cart(user=user)
                    cart.save()
                    messages.success(request, 'Account created successfully!')
                    return redirect('login')

    context = {
        'form': form,
        'form2': form2,
        'form3': form3,
        'messages': messages
    }
    return render(request, 'register.html', context)
