from django.db import models
from django.contrib.postgres.fields import ArrayField


class Jewelry(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to='images')
    description = models.TextField()
    category = models.CharField(max_length=20)
    metal = ArrayField(models.CharField(max_length=20))
    stone = ArrayField(models.CharField(max_length=20))
    care_tips = models.TextField()
    rating = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    sold = models.PositiveIntegerField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.CharField(max_length=50)

    def __str__(self):
        return self.user


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    jewelry = models.ForeignKey(Jewelry, on_delete=models.CASCADE)
    order_quantity = models.PositiveIntegerField()
    sub_total = models.DecimalField(max_digits=9, decimal_places=2)
