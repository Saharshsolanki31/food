from django.contrib import admin

# Register your models here.
from restaurant.models import type_of_restaurant, restaurant, dish_type, dish_category, food_item

admin.site.register(dish_type)
admin.site.register(type_of_restaurant)
admin.site.register(restaurant)
admin.site.register(dish_category)
admin.site.register(food_item)