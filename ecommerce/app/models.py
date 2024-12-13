from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    address=models.CharField(max_length=255,null=True)
    phone=models.CharField(max_length=255,null=True)
    image=models.ImageField(upload_to='images',null=True)

class Category(models.Model):
    catoegyname=models.CharField(max_length=255,null=True)

class Product(models.Model):
    productname=models.CharField(max_length=255,null=True)
    description=models.CharField(max_length=255,null=True)
    price=models.IntegerField(null=True)
    quantity=models.IntegerField(null=True)
    image=models.ImageField(upload_to='images',null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

class Cart(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    date=models.DateTimeField(null=True)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)