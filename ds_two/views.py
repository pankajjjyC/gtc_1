from django.shortcuts import render
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

# Create your views here.
def chart1(r):#indextwo
    context4=None
    csv=None
    df22=None
    z=None
    k=None
    fig3=None
    obj=None
    chart3=None
    queryset = Csv.objects.all()
    
    if queryset:
        if r.method=='POST':
            csv=r.POST['csv']
            obj = Csv.objects.latest('id')
            Csv.objects.filter(pk=obj).update(csv=csv)

        mydata22=[i.csv for i in queryset]
        
        df22 = read_csv(mydata22[-1])
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
    else:
        chart3 = "you haven't uploaded any files yet"
        context4={'chart_bar': chart3}
              
    
    return render(r, 'chart3.html', context4)
