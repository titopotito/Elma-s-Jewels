from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('cart', views.cart, name='cart'),
    path('cart/add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('cart/remove_from_cart/<int:cart_item_id>', views.remove_from_cart, name='remove_from_cart'),
    path('shop', views.shop, name='shop'),
    path('product/<str:category>/<int:product_id>', views.show_product, name='product'),
    path('checkout/<int:cart_id>', views.checkout, name='checkout'),
    path('checkout/add_to_checkout/<int:cart_id>', views.add_to_checkout, name='add_to_checkout'),
    path('shipping', views.shipping, name='shipping'),
    path('payment', views.payment, name='payment')
]