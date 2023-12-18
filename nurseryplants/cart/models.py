from django.db import models
from shop.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateField(auto_now_add=True)

    def subtotal(self):
        return self.quantity*self.product.price

class Gift(models.Model):
    gname=models.CharField(max_length=200)
    image = models.ImageField(upload_to='cart/gift', null=True, blank=True)

    def __str__(self):
        return self.gname

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_items=models.IntegerField()
    place=models.TextField(max_length=200)
    phone=models.CharField(max_length=200)

    order_status=models.CharField(max_length=20,default="pending")
    delivery_status=models.CharField(max_length=30,default="pending")
    date_added=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    def subtotal(self):
        return self.no_of_items*self.product.price

    def grandtotal(self):
        return self.no_of_items*self.product.price

class Account(models.Model):
    acctnumber=models.IntegerField()
    accttype=models.CharField(max_length=200)
    balance=models.IntegerField()

    def __str__(self):
        return str(self.acctnumber)


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.pname