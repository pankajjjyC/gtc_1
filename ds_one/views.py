from zlib import DEF_BUF_SIZE
from django.shortcuts import render , HttpResponse
import plotly.express as px
from core.models import CO2, Csvforheat , Csvfor_bar , Csvfor_heat , text
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
import sys
sys.path.append('C:\\Users\\pankaj\\Desktop\\GTC running app files\\git clone 2 copy\\django-plotly-integration\\ds_one')
import Aradiss as ad
from .Aradiss.abstraction import data
from .Aradiss.abstraction import correlations
path = os.getcwd()





def chart(request):#ds_one home url function view
    if request.method == 'POST':# csv file saving code
        file = request.FILES['fr']        
        id=request.POST['id']
        obj = Csvforheat(csv=file,id=id)
        obj.save()
        # csv file saving code ends here------------







        # code to select csv from models
        csv_obj_csvheat=Csvforheat.objects.first()
        df_table_data=csv_obj_csvheat.csv   
        
        csv_obj_csvbar=Csvfor_bar.objects.first()
        csv_bar_file=csv_obj_csvbar.csv        
        
       # code to select csv from models ends here-------






        # code to convert csv data to tabular form 
        csv_uploaded = df_table_data   # ref line no 40__This should point to the csv file you upload 
        df = ad.abstraction.data.load_dataset(csv_uploaded)
        tabular_form_context=df.to_html()
        # code to convert csv data to tabular form ends here ------





        
        # code for heatmap  
        steps = 2000
        scores = ad.abstraction.correlations.dtw_correlations(df, csv_uploaded, steps) 
        scores = (scores - 1) *(-1)
        
        column_header=list(scores.columns.values)
      
        heat_fig = px.imshow(scores,x=column_header)
        heat_fig_context = heat_fig.to_html()

        # code for heatmap  ends here -------------






        #code for bar chart
        
        obj_csv_bar_two=Csvfor_bar.objects.first()
        csv_bar_file_two=obj_csv_bar_two.csv
        csv_bar_file_two_readcsv = read_csv(csv_bar_file_two)
        data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

        data_frame_col_one=list(data_frame_bar.columns.values)
        
        fig_bar = px.bar(
        data_frame = data_frame_bar,
        x = data_frame_col_one[0],
       
        y = data_frame_col_one[1],
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )

        fig_bar_context = fig_bar.to_html()

        #code for bar chart ends here-----------------
        
        context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'chart66':fig_bar_context,'column_header':column_header}     

        
        return render(request, 'heatmap2.html',context_main)
    
    return render(request, 'chart.html')



def watchdemo(r):
    return render (r,'watchdemo.html')

def sample2(request):
    if request.method == 'POST':
        if request.POST.get('text'):
            savevalue=text()
            savevalue.text=request.POST.get('text')
            savevalue.id=request.POST.get('id')
            savevalue.save()

            # def chart() resources copied from above function-starts


            # code for selecting csv from models
            csv_obj_csvheat=Csvforheat.objects.first()
            df_table_data=csv_obj_csvheat.csv
            csv_obj_csvbar=Csvfor_bar.objects.first()
            csv_bar_file=csv_obj_csvbar.csv 
            # code for selecting csv from models ends here --------



            # code for making csv data to tabular form data 
            csv_uploaded = df_table_data   # This should point to the csv file you upload 
            df = ad.abstraction.data.load_dataset(csv_uploaded)            
            data_tabular_form=pd.DataFrame(df)
            tabular_form_context=data_tabular_form.to_html()
            # code for making csv data to tabular form data  end here --------


            # heat map code                  
            steps = 2000
            scores = ad.abstraction.correlations.dtw_correlations(df, csv_uploaded, steps) 
            scores = (scores - 1) *(-1) 

            column_header=list(scores.columns.values)        
            
            heat_fig = px.imshow(scores,x=column_header)
            heat_fig_context = heat_fig.to_html()
            # heat map code   ends here---------

            # bar chart code 
            obj_csv_bar_two=Csvfor_bar.objects.first()
            csv_bar_file_two=obj_csv_bar_two.csv
            csv_bar_file_two_readcsv = read_csv(csv_bar_file_two)

            obj_text_model=text.objects.first()# dropdown code
            text_file_selected_dropdown=obj_text_model.text
            
            te_fi_sel_dro_convrt_string=str(text_file_selected_dropdown)# dropdown code ends

            data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)
            data_frame_col_one=list(data_frame_bar.columns.values)#list of first column , not used presently
            
            fig_bar = px.bar(            
            data_frame = scores[te_fi_sel_dro_convrt_string],         
           
            opacity = 0.9,
            orientation = "v",
            barmode = 'group',
            title='',
            )

            fig_bar_context = fig_bar.to_html()
            # bar chart code ends here---------

            # def chart() resources copied from avove function-ends
            
            return render(request,'heatmap3.html',{'dfr': tabular_form_context, "chart555": heat_fig_context,'chart66':fig_bar_context,'column_header':column_header})
    else:
        return render(request,'heatmap3.html')







    


  








