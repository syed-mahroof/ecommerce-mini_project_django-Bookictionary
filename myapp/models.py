#models.py
from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    price=models.CharField(max_length=100,null=True, blank=True)
    description=models.CharField(max_length=1000,null=True, blank=True)
    image=models.ImageField(upload_to='images/',null=True, blank=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    price=models.CharField(max_length=100,null=True, blank=True)    
    quantity = models.IntegerField(null=True, default=1)
   

    def total_price(self):
        return float(self.price) * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    

class Register(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=100,null=True, blank=True)
    cpassword=models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.name
    