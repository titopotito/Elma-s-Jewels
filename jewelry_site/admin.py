from django.contrib import admin
from .models import Product, CartItem, Cart

class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'price', 'image', 'description', 'category', 'metal', 'stone', 'care_tips', 'rating', 'stock', 'sold']

class CartAdmin(admin.ModelAdmin):
    fields = ['user']

class CartItemAdmin(admin.ModelAdmin):
    fields = ['order_quantity']

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)