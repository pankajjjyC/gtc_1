from zlib import DEF_BUF_SIZE
from django.shortcuts import render , HttpResponse
import plotly.express as px
from core.models import CO2, Csvforheat , Csvfor_bar , Csvfor_heat , text , user_details
from pandas import read_csv
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User,auth 
from core.models import App_per_jesse
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

def signup(r):
    if r.method=='POST':
        username=r.POST['username']
        password=r.POST['password']

        email = r.POST['email']  
        reason=r.POST['reason']      
        block=r.POST['block']

        if User.objects.filter(username=username).exists():
            messages.info(r,'already exist')
            return redirect('signup')
        else:
            user=User.objects.create_user(username=username,password=password)
            user.save()
            user_detail=user_details(user_name=username,email=email,reason=reason,block_no=block)
            user_detail.save()
            messages.info(r,'User Created Successfully !')
            return redirect('login')
    else:
        return render(r,'signup.html',{})

def secure(r):
    obj=App_per_jesse.objects.get(id=1)    
    app1=obj.app_1 
    app2=obj.app_2
    app3=obj.app_3
    app4=obj.app_4
    app5=obj.app_5
    app6=obj.app_6     
    app7=obj.app_7
    app8=obj.app_8 

    obj2=App_per_jesse.objects.get(id=2)    
    ipp1=obj2.app_1 
    ipp2=obj2.app_2
    ipp3=obj2.app_3
    ipp4=obj2.app_4
    ipp5=obj2.app_5
    ipp6=obj2.app_6     
    ipp7=obj2.app_7
    ipp8=obj2.app_8 

    obj3=App_per_jesse.objects.get(id=3)    
    jpp1=obj3.app_1 
    jpp2=obj3.app_2
    jpp3=obj3.app_3
    jpp4=obj3.app_4
    jpp5=obj3.app_5
    jpp6=obj3.app_6     
    jpp7=obj3.app_7
    jpp8=obj3.app_8 

    obj4=App_per_jesse.objects.get(id=4)    
    ppp1=obj4.app_1 
    ppp2=obj4.app_2
    ppp3=obj4.app_3
    ppp4=obj4.app_4
    ppp5=obj4.app_5
    ppp6=obj4.app_6     
    ppp7=obj4.app_7
    ppp8=obj4.app_8 
    

    return render (r,'secure.html',{'app1':app1,'app2':app2,'app3':app3,'app4':app4,'app5':app5,'app6':app6,'app7':app7,'app8':app8,'ipp1':ipp1,'ipp2':ipp2,'ipp3':ipp3,'ipp4':ipp4,'ipp5':ipp5,'ipp6':ipp6,'ipp7':ipp7,'ipp8':ipp8,'jpp1':jpp1,'jpp2':jpp2,'jpp3':jpp3,'jpp4':jpp4,'jpp5':jpp5,'jpp6':jpp6,'jpp7':jpp7,'jpp8':jpp8,'ppp1':ppp1,'ppp2':ppp2,'ppp3':ppp3,'ppp4':ppp4,'ppp5':ppp5,'ppp6':ppp6,'ppp7':ppp7,'ppp8':ppp8})
    


def logout(r):
    auth.logout(r) 
    return redirect('login')


def sample(r):
    if r.method == 'POST':
        name=r.POST.get('full-name')
        email=r.POST.get('email')
        subject=r.POST.get('subject')
        message=r.POST.get('message')

        data={
            'name': name,
            'email': email,
            'subject': subject,
            'message': message

        }
        message='''
        New message: {}

        From: {}
        '''.format(data['message'],data['email'])
        send_mail(data['subject'],message,'', ['pankajrajoria05@gmail.com'])

    return render (r,'sample.html',{})

def sample2(request):
    
    column_header=[1,2,3,4,5,6]
    if request.method == 'POST':
        if request.POST.get('text'):
            savevalue=text()
            savevalue.text=request.POST.get('text')
            savevalue.save()
            messages.success(request,'saved')
            return render(request,'sample2.html')
    else:
        return render(request,'sample2.html',{'column_header':column_header})



