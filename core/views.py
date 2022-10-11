from asyncio.windows_events import NULL
from zlib import DEF_BUF_SIZE
from django.shortcuts import render , HttpResponse
import plotly.express as px
from core.models import   text , user_details
from pandas import read_csv
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User,auth 
from core.models import Permissions
from django.core.files.storage import FileSystemStorage
import os
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np
import pandas as pd
import csv
import numpy
from django.core.mail import send_mail
from django.conf import settings






def home(r):      
    return render(r,'home.html',{})


def login(r):
    if r.method=='POST':
        username=r.POST['username']
        password=r.POST['password']
        obj=auth.authenticate(r,username=username,password=password)
        if obj is not None:
            auth.login(r,obj)
            return redirect('secure')
        else:
            messages.info(r,'wrong credentials')
            return redirect('login')   
    return render(r,'login.html',{})

def signup_ara(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        block=request.POST['block']

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  ['pankajrajoria05@gmail.com'], fail_silently=False)

        user_detail=user_details(name=subject,email=email,reason=message,block_no=block)
        user_detail.save()
        return render(request, 'email_sent.html', {'email': email})

    return render (request,'signup_ara.html',{})


    

def secure(r):

    try:
        if r.user:        
            user_id = r.user.id #this will give currently logged in user id
            
            app_per_j=list(set(Permissions.objects.all().values_list('user_name','app_1','app_2','app_3','app_4','app_5','app_6','app_7','app_8')))

            current_user_lst=[]  
            current_index=None
            
            for i in app_per_j:
                for k in i:
                    if k == user_id:
                        current_index=app_per_j.index(i)

            current_user_lst.append(app_per_j[current_index])

            current_usr_list_filter=[]
            for i in current_user_lst:
                for k in i:
                    current_usr_list_filter.append(k)

            current_user_index=current_usr_list_filter[0]
            app1=current_usr_list_filter[1]
            app2=current_usr_list_filter[2]
            app3=current_usr_list_filter[3]
            app4=current_usr_list_filter[4]
            app5=current_usr_list_filter[5]
            app6=current_usr_list_filter[6]
            app7=current_usr_list_filter[7]
            app8=current_usr_list_filter[8]    
            
            return render (r,'secure.html',{'current_user_index':current_user_index,'app1':app1,'app2':app2,'app3':app3,'app4':app4,'app5':app5,'app6':app6,'app7':app7,'app8':app8,'apj':app_per_j,'user_id':user_id,'current_usr_list_filter':current_usr_list_filter,'current_index':current_index,'user_id':user_id}) 





    except Exception:
        return render(r,'secure.html')






    
    


def logout(r):
    auth.logout(r)
    x=text.objects.filter(id=15)
    x.update(text=NULL,battery_voltage=NULL,battery_current=NULL,no_of_operational=NULL,cut_off_thresold=NULL,remove_first_col=False) 
    return redirect('login')

def secure_(request):
    return render (request,'secure_offline.html',{}) 



def forgtpasswrd(request):
    if request.method == 'POST':
        subject = request.POST.get('email')
        message = request.POST.get('email')
        email = request.POST.get('email')

        usernames = User.objects.values_list('username', flat=True)
        obj_list=list(usernames)
        
        if subject in obj_list:
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                    [email], fail_silently=False)

            send_mail(subject, message, settings.EMAIL_HOST_USER,
                    ['pankajrajoria05@gmail.com'], fail_silently=False)
            return render(request, 'email_sent.html', {'email': email})
        else:
            return HttpResponse("user not registered")


        
        

    
    return render (request,'forgotpasswrd.html',{})


def sample(request):

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)
        return render(request, 'email_sent.html', {'email': email})

    return render (request,'sample.html',{})



def sample2(request):    
    if request.method == 'POST':
        savevalue=user_details()

        savevalue.id=request.POST.get('id')
        savevalue.save()
    return render (request,'sample2.html',{})


def sample3(request):
    return render (request,'sample3.html',{})


def signup_cas(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        block=request.POST['block']

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  ['pankajrajoria05@gmail.com'], fail_silently=False)

        user_detail=user_details(name=subject,email=email,reason=message,block_no=block)
        user_detail.save()
        return render(request, 'email_sent.html', {'email': email})

    return render (request,'signup_cas.html',{})



def signup_dis(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        block=request.POST['block']

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  ['pankajrajoria05@gmail.com'], fail_silently=False)

        user_detail=user_details(name=subject,email=email,reason=message,block_no=block)
        user_detail.save()
        return render(request, 'email_sent.html', {'email': email})

    return render (request,'signup_dis.html',{})


def signup_loc(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        block=request.POST['block']

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  ['pankajrajoria05@gmail.com'], fail_silently=False)

        user_detail=user_details(name=subject,email=email,reason=message,block_no=block)
        user_detail.save()
        return render(request, 'email_sent.html', {'email': email})

    return render (request,'signup_loc.html',{})



def signup_trac(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        block=request.POST['block']

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  ['pankajrajoria05@gmail.com'], fail_silently=False)

        user_detail=user_details(name=subject,email=email,reason=message,block_no=block)
        user_detail.save()
        return render(request, 'email_sent.html', {'email': email})

    return render (request,'signup_trac.html',{})



def signup_trat(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        block=request.POST['block']

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  ['pankajrajoria05@gmail.com'], fail_silently=False)

        user_detail=user_details(name=subject,email=email,reason=message,block_no=block)
        user_detail.save()
        return render(request, 'email_sent.html', {'email': email})

    return render (request,'signup_trat.html',{})



