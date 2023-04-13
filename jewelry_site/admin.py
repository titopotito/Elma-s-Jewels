from django.contrib import admin
from .models import Jewelry, CartItem, Cart, Order, OrderItem


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


class OrderAdmin(admin.ModelAdmin):
    fields = ['user', 'order_key', 'total_paid', 'payment_option']


class OrderItemAdmin(admin.ModelAdmin):
    fields = ['order', 'jewelry', 'price', 'quantity']


admin.site.register(Jewelry, JewelryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
