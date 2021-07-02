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
from user.models import user





# login function
def login(request):
    if 'user_email' in request.session:
        return redirect('home')
    else:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            if user.objects.filter(email=email).exists():
                if user.objects.filter(email=email, password=password).exists():
                    msg = "Login-In Successfuly!! "
                    my_user = user.objects.get(email=email)
                    request.session['user_email'] = email
                    request.session['user_name'] = my_user.name
                    messages.success(request,msg)
                    return redirect('index')
                else:
                    msg = "Inccorect Password !"
                    messages.success(request, msg)
                    return redirect(login)
            else:
                msg = "Email is Not Registered !"
                messages.success(request, msg)
                return redirect(register)
        else:
          return render(request, "user/login.html")







def register(request):
    if request.method=="POST":
        email=request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        if user.objects.filter(email=email).exists():
            msg="You have Already Registered !"
            messages.success(request,msg)
            return redirect(register)
        elif user.objects.filter(phone=phone).exists():
            msg = "Mobile Number is linked With Another Account !"
            messages.success(request, msg)
            return redirect(register)
        else:
            otp=random.randint(1000,9999)
            subject = "ONE TIME PASSWORD VERIFCTAION CODE"
            sender = settings.EMAIL_HOST_USER
            to = email
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
            request.session['email'] = email
            request.session['password'] = password
            request.session['phone'] = phone
            msg="We have sended you a one time password on your email !!"
            messages.success(request, msg)
            return redirect(verify_otp)
    else:
        return render(request,"user/registration_form.html")

#function for Otp Varification
def verify_otp(request):
    if request.method == "POST":
        email = request.session['email']
        password = request.session['password']
        phone = request.session['phone']
        otp_by_user=str(request.POST['otp_from_user'])
        otp_by_server=str(request.session['otp_from_server'])
        if otp_by_user!=otp_by_server:
            msg="The otp you have enter is incorect !!"
            messages.error(request,msg)
            return redirect(verify_otp)
        else:
            my_user=user(email=email,password=password,phone=phone)
            my_user.save()
            cont="Congratulation You Have Successfully registered"
            send_mail(
                "Registration Successfull",
                cont,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            msg="Your Account is created Now You Can Login"
            request.session.flush()
            messages.success(request,msg)
            return redirect(login)
    else:
        return render(request,'user/verify-otp.html')

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
        if user.objects.filter(email=email).exists():
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
        otp_by_user= str(request.POST['otp'])
        otp_by_server = str(request.session['otp_from_server'])
        if otp_by_user != otp_by_server:
            msg="incorrect Otp"
            return JsonResponse({'status':1,'msg':msg })
        else:
            user=user.objects.get(email=email)
            user.password=password
            user.save()
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




#function logoutuser data
def logout(request):
    #del request.session['user_name']
    #del request.session['user_email']
    request.session.flush()
    msg="logout Successfully"
    return render(request,'index.html',{'msg':msg})