from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('profile', views.profile, name='profile'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('cart', include([
        path('', views.cart_page, name='cart'),
        path('/add_cart_item/<int:jewelry_id>', views.add_cart_item, name='add_cart_item'),
        path('/delete_cart_item/<int:cart_item_id>', views.delete_cart_item, name='delete_cart_item'),
        path('/update_cart_item/<int:cart_item_id>', views.update_cart_item, name='update_cart_item')
    ])),


    path('shop', include([
        path('', views.shop_page, name='shop'),
        path('/jewelry/<int:jewelry_id>', views.jewelry_page, name='jewelry')

    ])),

    path('checkout', include([
        path('/<int:cart_id>', views.checkout, name='checkout'),
        path('/add_to_checkout/<int:cart_id>', views.add_to_checkout, name='add_to_checkout')
    ])),

    path('shipping', views.shipping, name='shipping'),
    path('payment', views.payment, name='payment')
]
