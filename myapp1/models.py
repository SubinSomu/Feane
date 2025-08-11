

from django.db import models


class FoodItem(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    price = models.IntegerField(max_length=10,blank=True,null=True)
    image = models.ImageField(upload_to='food_images/',blank=True,null=True)
    description = models.TextField(blank=True, null=True) 
    def __str__(self):
        return self.name
    

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.coupon_code} - {self.discount_percent}%"