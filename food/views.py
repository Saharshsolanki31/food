from django.shortcuts import render

#function For Home
def index(request):
    return  render(request,'index.html')