from django.shortcuts import render
import plotly.express as px
from ds_three.models import Csvforbar
from pandas import read_csv
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User,auth 
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
def chart2(r):#chart2 , block3 , ds_three 

    if r.method=='POST':
        csv=r.POST['csv']
        use=Csvforbar(csv=csv)
        use.save()   

    queryset = Csvforbar.objects.all()
    context4=None
    qq=None
    qq1=None
    qq2=None
    kk=None
    df22=None
    dataxy=None
    context4=None
    z=None
    k=None


    if queryset.exists():
        mydata22=[i.csv for i in queryset]
        qq=Csvforbar.objects.order_by('id').reverse()[0]
        qq1=str(qq)
        qq2=qq1[-2]
        kk = int(qq2)
        df22 = read_csv(mydata22[-1])
        z=df22['x']
        k=df22['y']
    else:
        context4='you do have uploaded csv files yet' 

   
    
    fig3 = px.line(
        x=z,
        y=k,
        title="X-Y Values",
        labels={'x': 'X values', 'y': 'Y values'}
    )

    chart3 = fig3.to_html()
    context4 = {'chart_line': chart3}
    return render(r, 'chart4.html', context4)
