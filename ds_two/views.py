from django.shortcuts import render , HttpResponse
import plotly.express as px
from ds_two.models import Csv 
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
from .forms import MyfileUploadForm


# Create your views here.
def chart1(request):#indextwo
    

    if request.method == 'POST':
        form = MyfileUploadForm(request.POST, request.FILES)
        #print(form.as_p)        
        if form.is_valid():            
            the_files = form.cleaned_data['files_data']
            t = Csv.objects.latest('id')
            t.csv = the_files  # change field
            t.save()
            #Csv(csv=the_files).save()            
            return redirect('bar')
        else:
            return HttpResponse('error')
    else:        
        context = {
            'form':MyfileUploadForm()
        }    
       
        return render(request, 'chart3.html', context)
              
    
    

def bar(r):
    tt = Csv.objects.first()
    csvv=tt.csv
    df22 = read_csv(csvv)
    z=df22['x']
    k=df22['y']   


    fig3 = px.bar(
    x=z,
    y=k,
    title="X-Y Values",
    labels={'x': 'X values', 'y': 'Y values'}
    )

    chart3 = fig3.to_html()
    context4 = {'chart_bar': chart3}
    return render(r, 'bar.html', context4)


