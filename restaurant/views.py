from django.shortcuts import render

# Create your views here.
import random
from datetime import datetime
import random
import string

from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template

from food import settings
from restaurant.models import restaurant, type_of_restaurant, dish_category, dish_type


# login function
def login(request):
    if 'restaurant_email' in request.session:
        return redirect('restaurant_home')
    else:
        if request.method == "POST":
            restaurant_email = request.POST['restaurant_email']
            restaurant_password = request.POST['restaurant_password']
            if restaurant.objects.filter(restaurant_email=restaurant_email).exists():
                if restaurant.objects.filter(restaurant_email=restaurant_email, restaurant_password=restaurant_password).exists():
                    msg = "Login-In Successfuly!! "
                    my_restaurant = restaurant.objects.get(restaurant_email=restaurant_email)
                    request.session['restaurant_email'] = restaurant_email
                    request.session['restaurant_name'] = my_restaurant.restaurant_name
                    messages.success(request,msg)
                    return redirect('restaurant_home')
                else:
                    msg = "Inccorect Password !"
                    messages.success(request, msg)
                    return redirect(login)
            else:
                msg = "Email is Not Registered !"
                messages.success(request, msg)
                return redirect(register)
        else:
          return render(request, "restaurant/login.html")


def restaurant_home(request):
    if 'restaurant_email' in request.session:
        return render(request,'restaurant/home.html')
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)


def menu(request):
    if 'restaurant_email' in request.session:
        if request.method == "POST":
            dish_types = dish_type.objects.get(id=request.POST[''])
            dish_cat = request.POST['dish_category']
        else:
            res_id = restaurant.objects.get(restaurant_email = request.session['restaurant_email'])
            dish_types = dish_type.objects.all()
            return render(request,'restaurant/menu.html',{'dish_type':dish_types})
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)

def add_dish_category(request):
    if 'restaurant_email' in request.session:

        return render(request,'restaurant/table.html')
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)



def table(request):
    if 'restaurant_email' in request.session:
        return render(request,'restaurant/table.html')
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)


def orders(request):
    if 'restaurant_email' in request.session:
        return render(request,'restaurant/orders.html')
    else:
        messages.error(request,'session expired ! Login Again')
        return  redirect(login)


def register(request):
    if request.method=="POST":
        restaurant_type = request.POST['restaurant_type']
        restaurant_name = request.POST['restaurant_name']
        restaurant_email = request.POST['restaurant_email']
        restaurant_mobile_number = request.POST['restaurant_mobile_number']
        restaurant_password = request.POST['restaurant_password']
        restaurant_address = request.POST['restaurant_address']
        restaurant_city = request.POST['restaurant_city']
        restaurant_state = request.POST['restaurant_state']
        restaurant_pincode = request.POST['restaurant_pincode']
        if restaurant.objects.filter(restaurant_email=restaurant_email).exists():
            msg="You have Already Registered !"
            messages.error(request,msg)
            return redirect(register)
        elif restaurant.objects.filter(restaurant_mobile_number=restaurant_mobile_number).exists():
            msg = "Mobile Number is linked With Another Account !"
            messages.error(request, msg)
            return redirect(register)
        else:
            otp=random.randint(1000,9999)
            subject = "ONE TIME PASSWORD VERIFCTAION CODE"
            sender = settings.EMAIL_HOST_USER
            to = restaurant_email
            title="OTP FOR EMAIL VERIFCATION"
            message="One Time Password For Your Account Regitration"
            ctx = {
                'title':title,
                'otp':otp,
                'content': message,
            }
            message = get_template('email_template/email_otp.html').render(ctx)
            msg = EmailMessage(
                subject,
                message,
                sender,
                [to],
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            request.session['otp_from_server']=otp
            request.session['restaurant_name'] = restaurant_name
            request.session['restaurant_email'] = restaurant_email
            request.session['restaurant_mobile_number'] = restaurant_mobile_number
            request.session['restaurant_password'] = restaurant_password
            request.session['restaurant_address'] = restaurant_address
            request.session['restaurant_city'] = restaurant_city
            request.session['restaurant_state'] = restaurant_state
            request.session['restaurant_pincode'] = restaurant_pincode
            request.session['restaurant_type'] = restaurant_type
            msg="We have sended you a one time password on your email !!"
            messages.success(request, msg)
            return redirect(verify_otp)
    else:
        restaurant_type = type_of_restaurant.objects.all()
        return render(request,"restaurant/registration_form.html",{'restaurant_type':restaurant_type})

#function for Otp Varification
def verify_otp(request):
    if request.method == "POST":
        restaurant_name = request.session['restaurant_name']
        restaurant_email =   request.session['restaurant_email']
        restaurant_mobile_number = request.session['restaurant_mobile_number']
        restaurant_password   =  request.session['restaurant_password']
        restaurant_address    =   request.session['restaurant_address']
        restaurant_city       =  request.session['restaurant_city']
        restaurant_state      =  request.session['restaurant_state']
        restaurant_pincode    =  request.session['restaurant_pincode']
        restaurant_type =request.session['restaurant_type']
        otp_by_restaurant=str(request.POST['otp_from_restaurant'])
        otp_by_server=str(request.session['otp_from_server'])
        if otp_by_restaurant!=otp_by_server:
            msg="The otp you have enter is incorect !!"
            messages.error(request,msg)
            return redirect(verify_otp)
        else:
            rest_type = type_of_restaurant.objects.get(id=int(restaurant_type))
            my_restaurant=restaurant(restaurant_name=restaurant_name,restaurant_type=rest_type,restaurant_email=restaurant_email,restaurant_password = restaurant_password,restaurant_mobile_number=restaurant_mobile_number,restaurant_address=restaurant_address,restaurant_city=restaurant_city,restaurant_state=restaurant_state,restaurant_pincode=restaurant_pincode)
            my_restaurant.save()
            cont="Congratulation You Have Successfully registered"
            send_mail(
                "Registration Successfull",
                cont,
                settings.EMAIL_HOST_USER,
                [restaurant_email],
                fail_silently=False,
            )
            msg="Your Account is created Now You Can Login"
            request.session.flush()
            messages.success(request,msg)
            return redirect(login)
    else:
        return render(request,'restaurant/verify-otp.html')

def resend_reg_otp(request):
   otp = random.randint(1000, 9999)
   subject = settings.site_name+" OTP For Email Verifcation"
   sender = settings.EMAIL_HOST_USER
   to = request.session['email']
   title = "Email Varification"
   message = "One Time Password For Your Account Regitration"
   ctx = {
                'title': title,
                'otp': otp,
                'content': message,
            }
   message = get_template('email_template/email_otp.html').render(ctx)
   msg = EmailMessage(
   subject,
   message,
   sender,
   [to],
            )
   msg.content_subtype = "html"  # Main content is now text/html
   msg.send()
   request.session['otp_from_server'] = otp
   msg='OTP Resended To Your Email Check Spam Folder '
   return JsonResponse({'status':0,'msg':msg})


def reset_password(request):
    if request.method=="POST":
        email=request.POST['email']
        if restaurant.objects.filter(email=email).exists():
            otp = random.randint(1000, 9999)
            subject = settings.EMAIL_HOST_USER
            sender = settings.site_name+"  OTP Verification"
            to = email
            title = "Email Varification"
            message = "Use The Below Code To Register Your Account "
            ctx = {
                'title': title,
                'otp': otp,
                'content': message,
            }
            message = get_template('email_template/email_otp.html').render(ctx)
            msg = EmailMessage(
                subject,
                message,
                sender,
                [to],
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            request.session['otp_from_server'] = otp
            request.session['email'] = email
            msg="Verification Code Sended To Your Email Check Spam Folder If Not Recived"
            return JsonResponse({'status':0,'msg':msg})
        else:
            #now We Need To Genrate 4 Digit Random Number And Send It To Mail
            msg = "The Email You Have Provided Is Not Registred With Us !! If Your New To Here You Need To Create Your Account First "
            return JsonResponse({'status':1,'msg':msg})
    else:
        return render(request,"forms/reset_password_form.html")

def varify_reset_password_otp(request):
    if request.method == "POST":
        email = request.session['email']
        password = request.POST['password']
        otp_by_restaurant= str(request.POST['otp'])
        otp_by_server = str(request.session['otp_from_server'])
        if otp_by_restaurant != otp_by_server:
            msg="incorrect Otp"
            return JsonResponse({'status':1,'msg':msg })
        else:
            restaurant=restaurant.objects.get(email=email)
            restaurant.password=password
            restaurant.save()
            request.session.flush()
            msg="Password Updated Successfully !! Redirecting You To Login"
            return JsonResponse({'status':0,'msg':msg })
    else:
        return render(request,'forms/reset_password_varify_otp.html')

def resend_reset_password_otp(request):
    otp = random.randint(1000, 9999)
    # code To Send Otp To Email
    subject = "OTP For Email Verifcation"
    sender = settings.EMAIL_HOST_USER
    to = request.session['email']
    title = "Email Varification"
    message = "One Time Password For Your Account Regitration"
    ctx = {
        'title': title,
        'otp': otp,
        'content': message,
    }
    message = get_template('email_template/email_otp.html').render(ctx)
    msg = EmailMessage(
        subject,
        message,
        sender,
        [to],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    request.session['otp_from_server'] = otp
    msgs="A New OTP Is Sended To Email Check Your Mail Check Spam Folder Also"
    return JsonResponse({'status':0,'msg':msgs })




#function logoutrestaurant data
def logout(request):
    request.session.flush()
    msg="logout Successfully"
    messages.success(request,msg)
    return redirect(login)