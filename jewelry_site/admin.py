from django.contrib import admin
from .models import Jewelry, CartItem, Cart


class JewelryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    fields = ['name', 'price', 'image', 'description', 'category',
              'metal', 'stone', 'care_tips', 'rating', 'stock', 'sold']


class CartAdmin(admin.ModelAdmin):
    fields = ['user']


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('get_jewelry_name', 'get_jewelry_price')
    fields = ['order_quantity', 'cart']

    def get_jewelry_name(self, obj):
        return obj.jewelry.name

    def get_jewelry_price(self, obj):
        return obj.jewelry.price


admin.site.register(Jewelry, JewelryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
