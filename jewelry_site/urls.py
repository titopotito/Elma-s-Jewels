from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart', views.cart, name='cart'),
    path('shop', views.shop, name='shop'),
    path('product', views.product, name='product'),
    path('checkout', views.checkout, name='checkout'),
    path('shipping', views.shipping, name='shipping'),
    path('payment', views.payment, name='payment')
]