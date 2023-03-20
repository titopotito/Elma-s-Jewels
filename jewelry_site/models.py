from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    jewelry = models.ForeignKey(Jewelry, on_delete=models.CASCADE)
    order_quantity = models.PositiveIntegerField()
    sub_total = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.jewelry.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.CharField(max_length=100, null=True, blank=True)
    building = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = CountryField()
    area_code = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class ContactDetail(models.Model):
    phone_number = PhoneNumberField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
