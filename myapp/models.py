from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from myapp1.models import FoodItem
from django.conf import settings




class MyUser(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)
    # usr = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    address=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.username


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('burger', 'Burger'),
        ('pizza', 'Pizza'),
        ('pasta', 'Pasta'),
        ('fries', 'Fries'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    full_name = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    date = models.DateField(blank=True,null=True)
    time = models.TimeField(blank=True,null=True)
    number_of_guests = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):
        return f'{self.full_name} - {self.date} at {self.time}'
class Register(models.Model):
    pass


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(FoodItem, on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.PositiveIntegerField(default=1)

 

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity


    