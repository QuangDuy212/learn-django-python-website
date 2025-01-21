from django.db import models
from django.contrib.auth.models import User


# Create your models here


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField()
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Shipping(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    company_name = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address


class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.customer.name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Cart {self.cart.id}"

    @property
    def Total(self):
        try:
            total = self.product.price * self.quantity
        except:
            total = self.product.price
        return total
