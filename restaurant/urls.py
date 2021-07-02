"""food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from restaurant import views

urlpatterns = [
    path('register',views.register,name="restaurant_registraion"),
    path('otp_verification',views.verify_otp,name="restaurant_otp_verification"),
    path('login',views.login,name="restaurant_login"),
    path('home',views.restaurant_home,name="restaurant_home"),
    path('menu',views.menu,name="restaurant_menu"),
    path('add_dish_category',views.add_dish_category,name='add_dish_category'),
    # path('menu/add/food',views.menu,name="restaurant_menu"),
    path('table',views.table,name="table"),
    path('orders',views.orders,name="orders"),
    path('logout',views.logout,name="logout"),
]
