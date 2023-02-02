from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Product, CartItem, Cart


def index(request):
    best_sellers = Product.objects.all().order_by('-sold')[:6]
    cart = Cart.objects.all()[0]
    return render(request, 'index.html', {'best_sellers':best_sellers, 'cart':cart})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


# CART ///////////////////////////////////////////////////////////

def cart(request):
    cart = Cart.objects.all()[0]
    cart_items = CartItem.objects.all()
    total_cost = 0
    if cart_items.count() > 0:
        for cart_item in cart_items:
            total_cost = total_cost + cart_item.sub_total 
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart':cart, 'total_cost': total_cost})

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.all()[0]
    cart_item = CartItem(cart=cart, product=product, order_quantity=1, sub_total=product.price)
    cart_item.save()
    return redirect('cart')

def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


# SHOP /////////////////////////////////////////////////////////////////////////////////

def shop(request):
    products = Product.objects.all().order_by('-sold')

    (products, category_options, metal_options, stone_options) = filter(request, products)
    

    sort_option = 'best-selling'
    if 'sort-option' in request.GET:
        sort_option = request.GET['sort-option']
        products = sort(sort_option, products)
    cart = Cart.objects.all()[0]

    paginator = Paginator(products, 16)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'products':paged_products, 
        'cart':cart, 
        'sort_option':sort_option, 
        'category_options':category_options, 
        'metal_options':metal_options, 
        'stone_options':stone_options
        }

    return render(request, 'shop.html', context)

def filter(request, products):
    category_options = []
    metal_options = []
    stone_options = []
    if 'category' in request.GET:
        category_options = request.GET.getlist('category')
        products = products.filter(category__in=category_options)
    if 'metal' in request.GET:
        metal_options = request.GET.getlist('metal')
        products = products.filter(metal__overlap=metal_options)
    if 'stone' in request.GET:
        stone_options = request.GET.getlist('stone')
        products = products.filter(stone__overlap=stone_options)
    return (products, category_options, metal_options, stone_options)

def sort(sort_option, products):
    if sort_option == 'best-selling':
        return products.order_by('-sold')
    elif sort_option == 'a-z':
        return products.order_by('name')
    elif sort_option == 'z-a':
        return products.order_by('-name')
    elif sort_option == 'low-high':
        return products.order_by('price')
    elif sort_option == 'high-low':
        return products.order_by('-price')
    elif sort_option == 'old-new':
        return products.order_by('date_added')
    elif sort_option == 'new-old':
        return products.order_by('-date_added')


def show_product(request, category, product_id):
    cart = Cart.objects.all()[0]
    product = Product.objects.get(pk=product_id)
    return render(request, 'product.html', {'product': product, 'cart':cart})



# PAYMENT ////////////////////////////////
def add_to_checkout(request, cart_id):
    return redirect('checkout', cart_id=cart_id)

def checkout(request, cart_id):
    return render(request, 'checkout.html')

def payment(request):
    return render(request, 'payment.html')

def shipping(request):
    return render(request, 'shipping.html')