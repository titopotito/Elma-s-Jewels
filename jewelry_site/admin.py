from django.contrib import admin
from .models import Jewelry, CartItem, Cart


class JewelryAdmin(admin.ModelAdmin):
    fields = ['name', 'price', 'image', 'description', 'category',
              'metal', 'stone', 'care_tips', 'rating', 'stock', 'sold']


class CartAdmin(admin.ModelAdmin):
    fields = ['user']


class CartItemAdmin(admin.ModelAdmin):
    fields = ['order_quantity', 'cart']


admin.site.register(Jewelry, JewelryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
