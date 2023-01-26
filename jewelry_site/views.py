from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def cart(request):
    return render(request, 'cart.html')

def shop(request):
    return render(request, 'shop.html')

def product(request):
    return render(request, 'product.html')

def checkout(request):
    return render(request, 'checkout.html')

def payment(request):
    return render(request, 'payment.html')

def shipping(request):
    return render(request, 'shipping.html')