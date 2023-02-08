from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Jewelry, CartItem, Cart


def index(request):
    best_sellers = Jewelry.objects.all().order_by('-sold')[:6]
    cart = Cart.objects.all()[0]
    return render(request, 'index.html', {'best_sellers': best_sellers, 'cart': cart, 'cart_item_count': CartItem.objects.all().count()})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# CART ///////////////////////////////////////////////////////////

def cart(request):
    cart = Cart.objects.all()[0]
    cart_items = CartItem.objects.all().order_by('id')
    total_cost = 0
    if cart_items.count() > 0:
        for cart_item in cart_items:
            total_cost = total_cost + \
                (cart_item.sub_total*cart_item.order_quantity)
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_item_count': CartItem.objects.all().count(), 'cart': cart, 'total_cost': total_cost})


def add_to_cart(request, jewelry_id):
    jewelry = Jewelry.objects.get(pk=jewelry_id)
    cart = Cart.objects.all()[0]
    cart_item = CartItem(cart=cart, jewelry=jewelry,
                         order_quantity=1, sub_total=jewelry.price)
    cart_item.save()
    return redirect('cart')


def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def update_order_quantity(request, cart_item_id):
    if int(request.POST['order-quantity']) == 0:
        print('here')
        remove_from_cart(request, cart_item_id)
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.order_quantity = request.POST['order-quantity']
    cart_item.save()
    return redirect('cart')

# SHOP /////////////////////////////////////////////////////////////////////////////////


def list_jewelry(request):
    jewelry = Jewelry.objects.all().order_by('-sold')

    (jewelry, category_options, metal_options,
     stone_options) = filter_jewelry(request, jewelry)

    sort_option = 'best-selling'
    if 'sort-option' in request.GET:
        sort_option = request.GET['sort-option']
        jewelry = sort_jewelry(sort_option, jewelry)

    paginator = Paginator(jewelry, 16)
    page = request.GET.get('page')
    paged_jewelry = paginator.get_page(page)
    context = {
        'jewelry': paged_jewelry,
        'cart': Cart.objects.all()[0],
        'cart_item_count': CartItem.objects.all().count(),
        'sort_option': sort_option,
        'category_options': category_options,
        'metal_options': metal_options,
        'stone_options': stone_options
    }

    return render(request, 'shop.html', context)


def filter_jewelry(request, jewelry):
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


def sort_jewelry(sort_option, jewelry):
    if sort_option == 'best-selling':
        return jewelry.order_by('-sold')
    elif sort_option == 'a-z':
        return jewelry.order_by('name')
    elif sort_option == 'z-a':
        return jewelry.order_by('-name')
    elif sort_option == 'low-high':
        return jewelry.order_by('price')
    elif sort_option == 'high-low':
        return jewelry.order_by('-price')
    elif sort_option == 'old-new':
        return jewelry.order_by('date_added')
    elif sort_option == 'new-old':
        return jewelry.order_by('-date_added')


def show_jewelry(request, jewelry_id):
    context = {
        'jewelry': Jewelry.objects.get(pk=jewelry_id),
        'cart': Cart.objects.all()[0],
        'cart_item_count': CartItem.objects.all().count()
    }
    return render(request, 'jewelry.html', context)


# PAYMENT ////////////////////////////////
def add_to_checkout(request, cart_id):
    return redirect('checkout', cart_id=cart_id)


def checkout(request, cart_id):
    return render(request, 'checkout.html')


def payment(request):
    return render(request, 'payment.html')


def shipping(request):
    return render(request, 'shipping.html')
