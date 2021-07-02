from django.db import models

# Create your models here.


class type_of_restaurant(models.Model):
    type_name = models.CharField(max_length=500)
    def __str__(self):
        return self.type_name




class restaurant(models.Model):
    restaurant_name = models.CharField(max_length=400)
    restaurant_email = models.CharField(max_length=400)
    restaurant_mobile_number = models.CharField(max_length=400)
    restaurant_logo = models.ImageField(upload_to='media/restaurant_logo',blank=True,null=True,default='media/restaurant_logo/default_logo.png')
    restaurant_password = models.CharField(max_length=400)
    restaurant_address = models.CharField(max_length=400)
    restaurant_city = models.CharField(max_length=400)
    restaurant_state = models.CharField(max_length=400)
    restaurant_pincode = models.CharField(max_length=400)
    restaurant_type = models.ForeignKey(type_of_restaurant,on_delete=models.CASCADE)
    def __str__(self):
        return self.restaurant_name


class dish_type(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name


class dish_category(models.Model):
    name = models.CharField(max_length=500)
    rest_id = models.ForeignKey(restaurant, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class food_item(models.Model):
    item_name = models.CharField(max_length=500)
    item_image = models.ImageField(upload_to='item_logo/',default='item_logo/logo.png'  )
    item_price = models.FloatField(max_length=500)
    restaurant_id = models.ForeignKey(restaurant, on_delete=models.CASCADE)
    dish_category = models.ForeignKey(dish_category,on_delete=models.CASCADE)
    dish_type = models.ForeignKey(dish_type,on_delete=models.CASCADE)
    def __str__(self):
        return self.item_name
