from django.shortcuts import render
import plotly.express as px
from core.models import CO2, Csvforheat 
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


# Create your views here.

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
        if User.objects.filter(username=username).exists():
            messages.info(r,'already exist')
            return redirect('signup')
        else:
            user=User.objects.create_user(username=username,password=password)
            user.save()
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
    #


def logout(r):
    auth.logout(r) 
    return redirect('/')








    




def chart(r):#indexthree
    
    if r.method=='POST':
        csv=r.POST['csv']
        use=Csvforheat(csv=csv)
        use.save()
        

    queryset = Csvforheat.objects.all()
    context4=None
    qq=None
    qq1=None
    qq2=None
    kk=None
    df22=None
    dataxy=None
    context4=None

    

    if queryset.exists():
        mydata22=[i.csv for i in queryset]
        qq=Csvforheat.objects.order_by('id').reverse()[0]
        qq1=str(qq)
        qq2=qq1[-2]
        kk = int(qq2)
        df22 = read_csv(mydata22[-1])
        dataxy = np.array(df22)
    else:
        context4='you do have uploaded csv files yet' 

     
    
    fig4 = px.imshow(dataxy)

    chart4 = fig4.to_html()
    context4 = {'chart_heat': chart4}
    return render(r, 'chart.html',context4)
  

