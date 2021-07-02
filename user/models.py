from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

# Model For User Data
class user(models.Model):
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=250,null=True)
    password = models.CharField(max_length=250)




# class user_query(models.Model):
#     name = models.CharField(max_length=250)
#     email = models.CharField(max_length=250)
#     subject = models.CharField(max_length=250)
#     message = models.CharField(max_length=250)