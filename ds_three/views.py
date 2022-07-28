from django.shortcuts import render , HttpResponse
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
from .formsss import MyfileUploadForm__

# Create your views here.
def chart2(request):#chart2 , block3 , ds_three 

    if request.method == 'POST':
        form = MyfileUploadForm__(request.POST, request.FILES)
        #print(form.as_p)        
        if form.is_valid():            
            the_files = form.cleaned_data['files_data__']
            t = Csvforbar.objects.latest('id')
            t.csv = the_files  # change field
            t.save()
            #Csv(csv=the_files).save()            
            return redirect('line')
        else:
            return HttpResponse('error')
    else:        
        context = {
            'form':MyfileUploadForm__()
        }    
       
        return render(request, 'chart4.html', context)



def line(r):
    ttt = Csvforbar.objects.first()
    csvv=ttt.csv
    df22 = read_csv(csvv)
    z=df22['x']
    k=df22['y'] 

    fig3 = px.line(
    x=z,
    y=k,
    title="X-Y Values",
    labels={'x': 'X values', 'y': 'Y values'}
    )

    
    chart4 = fig3.to_html()
    context4 = {'chart_line': chart4}
    return render(r, 'line.html',context4)