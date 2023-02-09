from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Address
from django_countries.fields import CountryField


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']


class CreateAddressForm(ModelForm):
    country = CountryField(blank_label='- Select Country -').formfield()

    class Meta:
        model = Address
        fields = ['unit', 'building', 'street', 'city', 'region', 'area_code', 'country']
