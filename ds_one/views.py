from asyncio.windows_events import NULL
from operator import is_not, le
from django.http import JsonResponse
from django.shortcuts import render , HttpResponse
import plotly.express as px
from core.models import  Csv_for_heat , Csv_for_heat , text , Identification_model , Csv_score_downld
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
import sys
sys.path.append('C:\\Users\\pankaj\\Desktop\\GTC running app files\\git clone 2 copy\\django-plotly-integration\\ds_one')
import Aradiss as ad
from .Aradiss.abstraction import data
from .Aradiss.abstraction import correlations
path = os.getcwd()

import ds_one.dash
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.figure_factory as ff

from io import StringIO
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View






def chart(request):#ds_one home url function view
    if request.method == 'POST':# csv file saving code        
        file = request.FILES['file_upload']        
        id=request.POST['id']
        obj = Csv_for_heat(csv=file,id=id)
        obj.save()
        # csv file saving code ends here------------



        # code to select csv from models
        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv   

        #comman_datafrme_without_process= pd.read_csv(df_table_data)
              
        
        #code to select csv from models ends here-------

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
        column_header2=list(scores.columns.values)

      
        heat_fig = px.imshow(scores,x=column_header,width=600, height=600)
        heat_fig_context = heat_fig.to_html()

        # code for heatmap  ends here -------------   

        #code for bar chart
        
        # csv_obj_csvbar=Csv_for_heat.objects.first()
        # Csv_for_heat.objects.first()
        csv_obj_csvbar=Csv_for_heat.objects.first()
        csv_bar_file=csv_obj_csvbar.csv  
        csv_bar_file_two_readcsv = read_csv(csv_bar_file)
        data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

        data_frame_col_names=list(df.columns.values)
        
        
        fig_bar = px.bar(            
            data_frame = scores,         
           
            opacity = 0.9,
            orientation = "v",
            barmode = 'group',
            title='',
            )
        fig_bar.update_yaxes(visible=False)
        fig_bar.update_xaxes(visible=False)
        fig_bar_context = fig_bar.to_html()

        #code for bar chart ends here-----------------

        # code for radio button yes no in data check
        list_radio = ["no", "yes"]
        temp4=text.objects.filter(id=1).values('remove_first_col')

        if temp4:
            answers_list_4 = list(temp4)
            finaloption_4=answers_list_4[0]
            selected_value_dropdown4=finaloption_4.get("remove_first_col") 
   
        else:
            selected_value_dropdown4='yes'

        
        # code for radio button yes no in data check......

        #code for several line charts
        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv    
        
        csv_uploaded = df_table_data    
        
        df2 = pd.read_csv(csv_uploaded) 
        data_frame_col_names2=list(df2.columns.values)
        len_of_uploadedcsv_col2=len(data_frame_col_names2)

        len_of_uploadedcsv_col=len(data_frame_col_names)

        em_list=[]    
        figures={}
        fig='fig'
        ele_context=None

        for num in range(1,len_of_uploadedcsv_col2):
            converted_num = str(num)
            fig=fig+converted_num
            em_list.append(fig)

        for j in range(0,len(em_list)):#len(em_list)
            em_list[j]=px.line(data_frame_bar,x=data_frame_col_names2[0], y=data_frame_col_names2[j],height=500,width=1200,).to_html()

        #code for several line charts end here.....

        # code for line charts 1 to 10 , .......
        em_list_1_10=[]    
        figures={}
        fig_1_10='fig'
        step=1
        link="chart_step2"

        for num in range(1,10):
            converted_num = str(num)
            fig_1_10=fig_1_10+converted_num
            em_list_1_10.append(fig_1_10)

        for j in range(1,len(em_list_1_10)):#len(em_list)
            em_list_1_10[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()
        # code for line charts 1 to 10 , .......ends here............        

        # code for many line charts, with two lines
        csv_obj_csvbar=Csv_for_heat.objects.first()
        csv_bar_file=csv_obj_csvbar.csv  
        csv_bar_file_two_readcsv = read_csv(csv_bar_file)
        data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv    
        
        csv_uploaded = df_table_data    
        
        df = ad.abstraction.data.load_dataset(csv_uploaded) 
        data_frame_col_names=list(df.columns.values)
        len_of_uploadedcsv_col=len(data_frame_col_names)

        em_list_fig_twolines=[]    
        figures={}
        fig='fig'
        ele_context=None

        for num in range(1,len_of_uploadedcsv_col):
            converted_num = str(num)
            fig=fig+converted_num
            em_list_fig_twolines.append(fig)

        for j in range(1,len(em_list_fig_twolines)):#len(em_list)   
            
            pdlineone= list(data_frame_bar[data_frame_col_names[0]])
            pdToList = list(data_frame_bar[data_frame_col_names[j]])        
            pdToList2 = []

            for i in pdToList:
                pdToList2.append(i+(i*0.1))

            trace0=go.Scatter(
                x=pdlineone,
                y=pdToList,
                mode='lines',            
            )

            trace1=go.Scatter(
                x=pdlineone,
                y=pdToList2,
                mode='lines',            
            )

            data=[trace0,trace1]
            layout=go.Layout(title='')

            #fig=go.Figure(data=data,layout=layout)
            em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html()    

        #context_main={'key':em_list_fig_twolines}  
        # code for many line charts, with two lines ends here..........................

        ###############################################################################
        ########################barchart for ML Performanve tab bar chart##############
        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv  
        csv_uploaded = df_table_data   
        df = ad.abstraction.data.load_dataset(csv_uploaded)   
        steps = 2000
        scores = ad.abstraction.correlations.dtw_correlations(df, csv_uploaded, steps) 
        scores = (scores - 1) *(-1)
        
    
            
        fig_bar1 = px.bar(            
            data_frame = scores, 
            width=1250,   
            height=500 ,    
            
            opacity = 1,
            orientation = "v",
            barmode = 'group',
            title='',
            )    
        fig_bar_context_b = fig_bar1.to_html()
        ##########################barchart for ML Performanve tab bar chart......ends#####
        ##################################################################################

        context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'chart66':fig_bar_context,
        'column_header':column_header,'column_header2':column_header2,'data_frame_col_one':data_frame_col_names,
        'data_frame_col_one':data_frame_col_names,'em_list':em_list,'em_list_fig_twolines':em_list_fig_twolines,
        'list_radio':list_radio,'selected_value_dropdown4':selected_value_dropdown4,
        'em_list_1_10':em_list_1_10,'step':step , 'link':link , 'fly':fig_bar_context_b,
        
        } 
       
        return render(request, 'try2.html',context_main)   
    return render(request, 'chart.html')


def charts(request):
    if request.method == 'POST':# csv file saving code        
        file = request.FILES['file_uploaded']        
        id=request.POST['id']
        obj = Identification_model(csv=file,id=id)
        obj.save()
        # csv file saving code ends here------------



        # code to select csv from models
        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv   

        #comman_datafrme_without_process= pd.read_csv(df_table_data)
              
        
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
        column_header2=list(scores.columns.values)

      
        heat_fig = px.imshow(scores,x=column_header,width=600, height=600)
        heat_fig_context = heat_fig.to_html()

        # code for heatmap  ends here -------------   

        ######
        # code for heatmap2 extra identification
        csv_obj_indent=Identification_model.objects.first()
        df_table_inden=csv_obj_indent.csv   

        csv_uploaded_iden = df_table_inden   

        df_iden = ad.abstraction.data.load_dataset(csv_uploaded_iden)
        tabular_form_context=df.to_html()     
        
        steps = 2000
        scores_iden = ad.abstraction.correlations.dtw_correlations(df_iden, csv_uploaded, steps) 
        scores_iden = (scores_iden - 1) *(-1)
        
        column_header_iden=list(scores_iden.columns.values)
        
        heat_fig_iden = px.imshow(scores_iden,x=column_header_iden,width=600, height=600)
        heat_fig_context_Iden= heat_fig_iden.to_html()
        # code for heatmap 2 exta identification ends here -------------  
        ######

        #####
        #code for bar chart exta identification.....  
        
        fig_bar_iden = px.bar(            
            data_frame = scores_iden['AccY (g)'],         
           
            opacity = 0.9,
            orientation = "v",
            barmode = 'group',
            title='',
            )
        fig_bar_iden.update_yaxes(visible=False)
        fig_bar_iden.update_xaxes(visible=False)
        fig_bar_context_iden = fig_bar_iden.to_html()

        #code for bar chart extra identification ends here-----------------
        #####
        # code for radio button yes no in data check
        list_radio = ["no", "yes"]
        temp4=text.objects.filter(id=14).values('remove_first_col')
        answers_list_4 = list(temp4)
        finaloption_4=answers_list_4[0]
        selected_value_dropdown4=finaloption_4.get("remove_first_col") 
        # code for radio button yes no in data check......

        #code for bar chart
        
        # csv_obj_csvbar=Csv_for_heat.objects.first()
        # Csv_for_heat.objects.first()
        csv_obj_csvbar=Csv_for_heat.objects.first()
        csv_bar_file=csv_obj_csvbar.csv  
        csv_bar_file_two_readcsv = read_csv(csv_bar_file)
        data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

        data_frame_col_names=list(df.columns.values)
        
        
        fig_bar = px.bar(            
            data_frame = scores['AccY (g)'],         
           
            opacity = 0.9,
            orientation = "v",
            barmode = 'group',
            title='',
            )
        fig_bar.update_yaxes(visible=False)
        fig_bar.update_xaxes(visible=False)
        fig_bar_context = fig_bar.to_html()
        

        #code for bar chart ends here-----------------

        #code for several line charts

        len_of_uploadedcsv_col=len(data_frame_col_names)

        em_list=[]    
        figures={}
        fig='fig'
        ele_context=None

        for num in range(1,len_of_uploadedcsv_col):
            converted_num = str(num)
            fig=fig+converted_num
            em_list.append(fig)

        for j in range(1,len(em_list)):#len(em_list)
            em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()

        #code for several line charts end here.....

        # code for many line charts, with two lines
        csv_obj_csvbar=Csv_for_heat.objects.first()
        csv_bar_file=csv_obj_csvbar.csv  
        csv_bar_file_two_readcsv = read_csv(csv_bar_file)
        data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv    
        
        csv_uploaded = df_table_data    
        
        df = ad.abstraction.data.load_dataset(csv_uploaded) 
        data_frame_col_names=list(df.columns.values)
        len_of_uploadedcsv_col=len(data_frame_col_names)

        em_list_fig_twolines=[]    
        figures={}
        fig='fig'
        ele_context=None

        for num in range(1,len_of_uploadedcsv_col):
            converted_num = str(num)
            fig=fig+converted_num
            em_list_fig_twolines.append(fig)

        for j in range(1,len(em_list_fig_twolines)):#len(em_list)   
            
            pdlineone= list(data_frame_bar[data_frame_col_names[0]])
            pdToList = list(data_frame_bar[data_frame_col_names[j]])        
            pdToList2 = []

            for i in pdToList:
                pdToList2.append(i+(i*0.1))

            trace0=go.Scatter(
                x=pdlineone,
                y=pdToList,
                mode='lines',            
            )

            trace1=go.Scatter(
                x=pdlineone,
                y=pdToList2,
                mode='lines',            
            )

            data=[trace0,trace1]
            layout=go.Layout(title='Average Home Goals by Year')

            #fig=go.Figure(data=data,layout=layout)
            em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html()    

        #context_main={'key':em_list_fig_twolines}  
        # code for many line charts, with two lines ends here..........................

        context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'heat_fig_context_Iden':heat_fig_context_Iden,'chart66':fig_bar_context,'fig_bar_context_iden':fig_bar_context_iden,
        'column_header':column_header,'column_header2':column_header2,'data_frame_col_one':data_frame_col_names,
        'data_frame_col_one':data_frame_col_names,'em_list':em_list,'em_list_fig_twolines':em_list_fig_twolines,
        'list_radio':list_radio,'selected_value_dropdown4':selected_value_dropdown4,
        
        } 
       
        return render(request, 'try2.html',context_main) 
    return render(request,'charts.html')



def chart_step2(request):       
    
    # code to select csv from models
    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv   

                   
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
    column_header2=list(scores.columns.values)

    
    heat_fig = px.imshow(scores,x=column_header,width=600, height=600)
    heat_fig_context = heat_fig.to_html()

    # code for heatmap  ends here -------------   

    ######
    # code for heatmap2 extra identification
    csv_obj_indent=Identification_model.objects.first()
    df_table_inden=csv_obj_indent.csv   

    csv_uploaded_iden = df_table_inden   

    df_iden = ad.abstraction.data.load_dataset(csv_uploaded_iden)
    tabular_form_context=df.to_html()     
    
    steps = 2000
    scores_iden = ad.abstraction.correlations.dtw_correlations(df_iden, csv_uploaded, steps) 
    scores_iden = (scores_iden - 1) *(-1)
    
    column_header_iden=list(scores_iden.columns.values)
    
    heat_fig_iden = px.imshow(scores_iden,x=column_header_iden,width=600, height=600)
    heat_fig_context_Iden= heat_fig_iden.to_html()
    # code for heatmap 2 exta identification ends here -------------  
    ######

    #####
    #code for bar chart exta identification.....  
    
    fig_bar_iden = px.bar(            
        data_frame = scores_iden['AccY (g)'],         
        
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
    fig_bar_iden.update_yaxes(visible=False)
    fig_bar_iden.update_xaxes(visible=False)
    fig_bar_context_iden = fig_bar_iden.to_html()

    #code for bar chart extra identification ends here-----------------
    #####
    # code for radio button yes no in data check
    list_radio = ["no", "yes"]
    temp4=text.objects.filter(id=1).values('remove_first_col')
    answers_list_4 = list(temp4)
    finaloption_4=answers_list_4[0]
    selected_value_dropdown4=finaloption_4.get("remove_first_col") 
    # code for radio button yes no in data check......

    #code for bar chart
    
    # csv_obj_csvbar=Csv_for_heat.objects.first()
    # Csv_for_heat.objects.first()
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    data_frame_col_names=list(df.columns.values)
    
    
    fig_bar = px.bar(            
        data_frame = scores,         
        
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
    fig_bar.update_yaxes(visible=False)
    fig_bar.update_xaxes(visible=False)
    fig_bar_context = fig_bar.to_html()

    #code for bar chart ends here-----------------

    #code for several line charts

    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list=[]    
    figures={}
    fig='fig'
    ele_context=None    

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list.append(fig)

    for j in range(1,len(em_list)):#len(em_list)
        em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()

    #code for several line charts end here.....

    # code for line charts 1 to 10 , .......
    em_list_1_10=[]    
    figures={}
    fig_1_10='fig'
    step=2
    link="chart_step3"
    tempvar=len_of_uploadedcsv_col-9
    lastseen=data_frame_col_names[9]
    if len_of_uploadedcsv_col>=8:
        for num in range(1,10):
            converted_num = str(num)
            fig_1_10=fig_1_10+converted_num
            em_list_1_10.append(fig_1_10)

        for j in range(1,len(em_list_1_10)):#len(em_list)
            em_list_1_10[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j+8],height=500,width=1200,).to_html()
    # code for line charts 1 to 10 , .......ends here............  

    # code for many line charts, with two lines
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv    
    
    csv_uploaded = df_table_data    
    
    df = ad.abstraction.data.load_dataset(csv_uploaded) 
    data_frame_col_names=list(df.columns.values)
    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list_fig_twolines=[]    
    figures={}
    fig='fig'
    ele_context=None

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list_fig_twolines.append(fig)

    for j in range(1,len(em_list_fig_twolines)):#len(em_list)   
        
        pdlineone= list(data_frame_bar[data_frame_col_names[0]])
        pdToList = list(data_frame_bar[data_frame_col_names[j]])        
        pdToList2 = []

        for i in pdToList:
            pdToList2.append(i+(i*0.1))

        trace0=go.Scatter(
            x=pdlineone,
            y=pdToList,
            mode='lines',            
        )

        trace1=go.Scatter(
            x=pdlineone,
            y=pdToList2,
            mode='lines',            
        )

        data=[trace0,trace1]
        layout=go.Layout(title='')

        #fig=go.Figure(data=data,layout=layout)
        em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html()    

    #context_main={'key':em_list_fig_twolines}  
    # code for many line charts, with two lines ends here..........................

    context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'heat_fig_context_Iden':heat_fig_context_Iden,'chart66':fig_bar_context,'fig_bar_context_iden':fig_bar_context_iden,
    'column_header':column_header,'column_header2':column_header2,'data_frame_col_one':data_frame_col_names,
    'data_frame_col_one':data_frame_col_names,'em_list':em_list,'em_list_fig_twolines':em_list_fig_twolines,
    'list_radio':list_radio,'selected_value_dropdown4':selected_value_dropdown4 , 'step':step,'len_of_uploadedcsv_col':len_of_uploadedcsv_col,
    'em_list_1_10':em_list_1_10,'len_of_uploadedcsv_col':len_of_uploadedcsv_col,'tempvar':tempvar,'lastseen':lastseen
    
    } 
    
    return render(request, 'try2.html',context_main) 



def chart_step3(request):       
    
    # code to select csv from models
    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv   

                   
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
    column_header2=list(scores.columns.values)

    
    heat_fig = px.imshow(scores,x=column_header,width=600, height=600)
    heat_fig_context = heat_fig.to_html()

    # code for heatmap  ends here -------------   

    ######
    # code for heatmap2 extra identification
    csv_obj_indent=Identification_model.objects.first()
    df_table_inden=csv_obj_indent.csv   

    csv_uploaded_iden = df_table_inden   

    df_iden = ad.abstraction.data.load_dataset(csv_uploaded_iden)
    tabular_form_context=df.to_html()     
    
    steps = 2000
    scores_iden = ad.abstraction.correlations.dtw_correlations(df_iden, csv_uploaded, steps) 
    scores_iden = (scores_iden - 1) *(-1)
    
    column_header_iden=list(scores_iden.columns.values)
    
    heat_fig_iden = px.imshow(scores_iden,x=column_header_iden,width=600, height=600)
    heat_fig_context_Iden= heat_fig_iden.to_html()
    # code for heatmap 2 exta identification ends here -------------  
    ######

    #####
    #code for bar chart exta identification.....  
    
    fig_bar_iden = px.bar(            
        data_frame = scores_iden['AccY (g)'],         
        
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
    fig_bar_iden.update_yaxes(visible=False)
    fig_bar_iden.update_xaxes(visible=False)
    fig_bar_context_iden = fig_bar_iden.to_html()

    #code for bar chart extra identification ends here-----------------
    #####
    # code for radio button yes no in data check
    list_radio = ["no", "yes"]
    temp4=text.objects.filter(id=1).values('remove_first_col')
    answers_list_4 = list(temp4)
    finaloption_4=answers_list_4[0]
    selected_value_dropdown4=finaloption_4.get("remove_first_col") 
    # code for radio button yes no in data check......

    #code for bar chart
    
    # csv_obj_csvbar=Csv_for_heat.objects.first()
    # Csv_for_heat.objects.first()
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    data_frame_col_names=list(df.columns.values)
    
    
    fig_bar = px.bar(            
        data_frame = scores,         
        
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
    fig_bar.update_yaxes(visible=False)
    fig_bar.update_xaxes(visible=False)
    fig_bar_context = fig_bar.to_html()

    #code for bar chart ends here-----------------

    #code for several line charts

    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list=[]    
    figures={}
    fig='fig'
    ele_context=None

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list.append(fig)

    for j in range(1,len(em_list)):#len(em_list)
        em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()

    #code for several line charts end here.....

    # code for line charts 1 to 10 , .......
    em_list_1_10=[]    
    figures={}
    fig_1_10='fig'
    step=3
    link="chart_step4"
    tempvar=len_of_uploadedcsv_col-16
    lastseen=data_frame_col_names[9]
    if len_of_uploadedcsv_col>=16:
        for num in range(1,tempvar):
            converted_num = str(num)
            fig_1_10=fig_1_10+converted_num
            em_list_1_10.append(fig_1_10)

        for j in range(1,len(em_list_1_10)):#len(em_list)
            em_list_1_10[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[16+(tempvar-2)],height=500,width=1200,).to_html()
    # code for line charts 1 to 10 , .......ends here............  

    # code for many line charts, with two lines
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv    
    
    csv_uploaded = df_table_data    
    
    df = ad.abstraction.data.load_dataset(csv_uploaded) 
    data_frame_col_names=list(df.columns.values)
    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list_fig_twolines=[]    
    figures={}
    fig='fig'
    ele_context=None

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list_fig_twolines.append(fig)

    for j in range(1,len(em_list_fig_twolines)):#len(em_list)   
        
        pdlineone= list(data_frame_bar[data_frame_col_names[0]])
        pdToList = list(data_frame_bar[data_frame_col_names[j]])        
        pdToList2 = []

        for i in pdToList:
            pdToList2.append(i+(i*0.1))

        trace0=go.Scatter(
            x=pdlineone,
            y=pdToList,
            mode='lines',            
        )

        trace1=go.Scatter(
            x=pdlineone,
            y=pdToList2,
            mode='lines',            
        )

        data=[trace0,trace1]
        layout=go.Layout(title='')

        #fig=go.Figure(data=data,layout=layout)
        em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html()    

    #context_main={'key':em_list_fig_twolines}  
    # code for many line charts, with two lines ends here..........................

    context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'heat_fig_context_Iden':heat_fig_context_Iden,'chart66':fig_bar_context,'fig_bar_context_iden':fig_bar_context_iden,
    'column_header':column_header,'column_header2':column_header2,'data_frame_col_one':data_frame_col_names,
    'data_frame_col_one':data_frame_col_names,'em_list':em_list,'em_list_fig_twolines':em_list_fig_twolines,
    'list_radio':list_radio,'selected_value_dropdown4':selected_value_dropdown4 , 'step':step,
    'em_list_1_10':em_list_1_10,'tempvar':tempvar
    
    } 
    
    return render(request, 'try2.html',context_main)




def chart_step4(request):       
    
    # code to select csv from models
    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv   

                   
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
    column_header2=list(scores.columns.values)

    
    heat_fig = px.imshow(scores,x=column_header,width=600, height=600)
    heat_fig_context = heat_fig.to_html()

    # code for heatmap  ends here -------------   

    ######
    # code for heatmap2 extra identification
    csv_obj_indent=Identification_model.objects.first()
    df_table_inden=csv_obj_indent.csv   

    csv_uploaded_iden = df_table_inden   

    df_iden = ad.abstraction.data.load_dataset(csv_uploaded_iden)
    tabular_form_context=df.to_html()     
    
    steps = 2000
    scores_iden = ad.abstraction.correlations.dtw_correlations(df_iden, csv_uploaded, steps) 
    scores_iden = (scores_iden - 1) *(-1)
    
    column_header_iden=list(scores_iden.columns.values)
    
    heat_fig_iden = px.imshow(scores_iden,x=column_header_iden,width=600, height=600)
    heat_fig_context_Iden= heat_fig_iden.to_html()
    # code for heatmap 2 exta identification ends here -------------  
    ######

    #####
    #code for bar chart exta identification.....  
    
    fig_bar_iden = px.bar(            
        data_frame = scores_iden['AccY (g)'],         
        
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
    fig_bar_iden.update_yaxes(visible=False)
    fig_bar_iden.update_xaxes(visible=False)
    fig_bar_context_iden = fig_bar_iden.to_html()

    #code for bar chart extra identification ends here-----------------
    #####
    # code for radio button yes no in data check
    list_radio = ["no", "yes"]
    temp4=text.objects.filter(id=14).values('remove_first_col')
    answers_list_4 = list(temp4)
    finaloption_4=answers_list_4[0]
    selected_value_dropdown4=finaloption_4.get("remove_first_col") 
    # code for radio button yes no in data check......

    #code for bar chart
    
    # csv_obj_csvbar=Csv_for_heat.objects.first()
    # Csv_for_heat.objects.first()
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    data_frame_col_names=list(df.columns.values)
    
    
    fig_bar = px.bar(            
        data_frame = scores['AccY (g)'],         
        
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
    fig_bar.update_yaxes(visible=False)
    fig_bar.update_xaxes(visible=False)
    fig_bar_context = fig_bar.to_html()

    #code for bar chart ends here-----------------

    #code for several line charts

    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list=[]    
    figures={}
    fig='fig'
    ele_context=None

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list.append(fig)

    for j in range(1,len(em_list)):#len(em_list)
        em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()

    #code for several line charts end here.....

    # code for line charts 1 to 10 , .......
    em_list_1_10=[]    
    figures={}
    fig_1_10='fig'
    step=4
    link="chart_step4"
    tempvar=len_of_uploadedcsv_col-9
    lastseen=data_frame_col_names[9]
    if len_of_uploadedcsv_col>=24:
        for num in range(1,10):
            converted_num = str(num)
            fig_1_10=fig_1_10+converted_num
            em_list_1_10.append(fig_1_10)

        for j in range(1,len(em_list_1_10)):#len(em_list)
            em_list_1_10[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j+24],height=500,width=1200,).to_html()
    # code for line charts 1 to 10 , .......ends here............  

    # code for many line charts, with two lines
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv    
    
    csv_uploaded = df_table_data    
    
    df = ad.abstraction.data.load_dataset(csv_uploaded) 
    data_frame_col_names=list(df.columns.values)
    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list_fig_twolines=[]    
    figures={}
    fig='fig'
    ele_context=None

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list_fig_twolines.append(fig)

    for j in range(1,len(em_list_fig_twolines)):#len(em_list)   
        
        pdlineone= list(data_frame_bar[data_frame_col_names[0]])
        pdToList = list(data_frame_bar[data_frame_col_names[j]])        
        pdToList2 = []

        for i in pdToList:
            pdToList2.append(i+(i*0.1))

        trace0=go.Scatter(
            x=pdlineone,
            y=pdToList,
            mode='lines',            
        )

        trace1=go.Scatter(
            x=pdlineone,
            y=pdToList2,
            mode='lines',            
        )

        data=[trace0,trace1]
        layout=go.Layout(title='')

        #fig=go.Figure(data=data,layout=layout)
        em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html()    

    #context_main={'key':em_list_fig_twolines}  
    # code for many line charts, with two lines ends here..........................

    context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'heat_fig_context_Iden':heat_fig_context_Iden,'chart66':fig_bar_context,'fig_bar_context_iden':fig_bar_context_iden,
    'column_header':column_header,'column_header2':column_header2,'data_frame_col_one':data_frame_col_names,
    'data_frame_col_one':data_frame_col_names,'em_list':em_list,'em_list_fig_twolines':em_list_fig_twolines,
    'list_radio':list_radio,'selected_value_dropdown4':selected_value_dropdown4 , 'step':step,
    'em_list_1_10':em_list_1_10
    
    } 
    
    return render(request, 'try2.html',context_main)

    




def samplesave(request):
    if request.method == 'POST':     
        battery_current=request.POST.get('bat_cur')
        battery_voltage=request.POST.get('bat_vol')        
        remove_first_col=request.POST.get('remove_first_col')
        id=request.POST.get('id')  
        query= text.objects.filter(id=1)
        if query:
            text.objects.filter(id=1).update(battery_current=battery_current,battery_voltage=battery_voltage,remove_first_col=remove_first_col,id=id)
        else:
            b = text(battery_current=battery_current,battery_voltage=battery_voltage,remove_first_col=remove_first_col,id=id)
            b.save()


        # def chart() resources copied from above function-starts


        # code to select csv from models
        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv   

        #comman_datafrme_without_process= pd.read_csv(df_table_data)
            
        
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
        column_header2=list(scores.columns.values)     
        
        heat_fig = px.imshow(scores,x=column_header,width=600, height=600)
        heat_fig_context = heat_fig.to_html()

        # code for heatmap  ends here ------------- 

                    
        #selected dropdown code 
        # dropdown one
        temp2=text.objects.filter(id=1).values('battery_current')
        answers_list = list(temp2)
        finaloption=answers_list[0]
        selected_value_dropdown_cur=finaloption.get("battery_current")

        temp3=text.objects.filter(id=1).values('battery_voltage')
        answers_list_3 = list(temp3)
        finaloption_3=answers_list_3[0]
        selected_value_dropdown_vol=finaloption_3.get("battery_voltage")

        list_radio = ["no", "yes"]
        temp4=text.objects.filter(id=1).values('remove_first_col')
        answers_list_4 = list(temp4)
        finaloption_4=answers_list_4[0]
        selected_value_dropdown_colmn=finaloption_4.get("remove_first_col") 
        # code for radio button yes no in data check......
        #selected dropdown code  ends here.... ...............................................................




        #code for bar chart   
    
        csv_obj_csvbar=Csv_for_heat.objects.first()
        csv_bar_file=csv_obj_csvbar.csv  
        csv_bar_file_two_readcsv = read_csv(csv_bar_file)
        data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

        data_frame_col_names=list(df.columns.values)
        
        obj_text_model=text.objects.first()
        dropdown_selected_bat_cur=obj_text_model.battery_current    
        dropdown_selected_bat_cur_convrt_string=str(dropdown_selected_bat_cur)

       
        if dropdown_selected_bat_cur_convrt_string == '0':
            dropdown_selected_bat_cur_convrt_string = data_frame_col_names[0]            
        elif dropdown_selected_bat_cur_convrt_string == 'None':
            dropdown_selected_bat_cur_convrt_string = data_frame_col_names[0]                       
        
               
        
        fig_bar = px.bar(               
        data_frame = scores[dropdown_selected_bat_cur_convrt_string], 
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
        fig_bar.update_yaxes(visible=False)
        fig_bar.update_layout(showlegend=False)

        fig_bar_context = fig_bar.to_html()
       

        #code for bar chart ends here-----------------

        #code for several line charts

        len_of_uploadedcsv_col=len(data_frame_col_names)

        em_list=[]    
        figures={}
        fig='fig'
        ele_context=None

        for num in range(1,len_of_uploadedcsv_col):
            converted_num = str(num)
            fig=fig+converted_num
            em_list.append(fig)

        for j in range(1,len(em_list)):#len(em_list)
            em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()

        #code for several line charts end here.....


        # code for many line charts, with two lines
        csv_obj_csvbar=Csv_for_heat.objects.first()
        csv_bar_file=csv_obj_csvbar.csv  
        csv_bar_file_two_readcsv = read_csv(csv_bar_file)
        data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv    
        
        csv_uploaded = df_table_data    
        
        df = ad.abstraction.data.load_dataset(csv_uploaded) 
        data_frame_col_names=list(df.columns.values)
        len_of_uploadedcsv_col=len(data_frame_col_names)

        em_list_fig_twolines=[]    
        figures={}
        fig='fig'
        ele_context=None

        for num in range(1,len_of_uploadedcsv_col):
            converted_num = str(num)
            fig=fig+converted_num
            em_list_fig_twolines.append(fig)

        for j in range(1,len(em_list_fig_twolines)):#len(em_list)   
            
            pdlineone= list(data_frame_bar[data_frame_col_names[0]])
            pdToList = list(data_frame_bar[data_frame_col_names[j]])        
            pdToList2 = []

            for i in pdToList:
                pdToList2.append(i+(i*0.1))

            trace0=go.Scatter(
                x=pdlineone,
                y=pdToList,
                mode='lines',            
            )

            trace1=go.Scatter(
                x=pdlineone,
                y=pdToList2,
                mode='lines',            
            )

            data=[trace0,trace1]
            layout=go.Layout(title='Average Home Goals by Year')

            #fig=go.Figure(data=data,layout=layout)
            em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html()    

        #context_main={'key':em_list_fig_twolines}  
        # code for many line charts, with two lines ends here..........................
        #######################################################################################################
        #######chart1 function code pasted here
        #######################################################################################################
        # code to select csv from models
        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv   

        #comman_datafrme_without_process= pd.read_csv(df_table_data)
        
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
        
        heat_fig = px.imshow(scores,x=column_header,width=600, height=600)
        heat_fig_context = heat_fig.to_html()

        # code for heatmap  ends here -------------




        # code to save csv scores in Csv_score model -------------        
        
        x=scores.to_csv(encoding='utf-8', index=False)

        temp_query=Csv_score_downld.objects.filter(id=1)

        if temp_query:
            Csv_score_downld.objects.filter(id=1).update(csv=x,id=1)
        else:
            c = Csv_score_downld(csv=x,id=1)
            c.save()
        
        notes=Csv_score_downld.objects.all()

        # code to save csv scores in Csv_score model__ ends here -------------

        

        #code for bar chart   
        
        csv_obj_csvbar=Csv_for_heat.objects.first()
        csv_bar_file=csv_obj_csvbar.csv  
        csv_bar_file_two_readcsv = read_csv(csv_bar_file)
        data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

        data_frame_col_names=list(df.columns.values)

        #custom bar chart saved from bat_cur dropdown code
        obj_text_model=text.objects.first()
        dropdown_selected_bat_cur=obj_text_model.battery_current    
        dropdown_selected_bat_cur_convrt_string=str(dropdown_selected_bat_cur)

        if dropdown_selected_bat_cur_convrt_string == '0':
            dropdown_selected_bat_cur_convrt_string = data_frame_col_names[0]
        elif dropdown_selected_bat_cur_convrt_string == 'None':
            dropdown_selected_bat_cur_convrt_string = data_frame_col_names[0]

        
        
        fig_bar = px.bar(            
        data_frame = scores[dropdown_selected_bat_cur_convrt_string],         
        
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
        fig_bar.update_yaxes(visible=False)
        fig_bar.update_layout(showlegend=False)

        fig_bar_context = fig_bar.to_html()
        ###################################

        #code for bar chart ends here-----------------

        #code for several line charts

        len_of_uploadedcsv_col=len(data_frame_col_names)

        em_list=[]    
        figures={}
        fig='fig'
        ele_context=None

        for num in range(1,len_of_uploadedcsv_col):
            converted_num = str(num)
            fig=fig+converted_num
            em_list.append(fig)

        for j in range(1,len(em_list)):#len(em_list)
            em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()

        #code for several line charts end here.....


        # code for many line charts, with two lines
        csv_obj_csvbar=Csv_for_heat.objects.first()
        csv_bar_file=csv_obj_csvbar.csv  
        csv_bar_file_two_readcsv = read_csv(csv_bar_file)
        data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv    
        
        csv_uploaded = df_table_data    
        
        df = ad.abstraction.data.load_dataset(csv_uploaded) 
        data_frame_col_names=list(df.columns.values)
        len_of_uploadedcsv_col=len(data_frame_col_names)

        em_list_fig_twolines=[]    
        figures={}
        fig='fig'
        ele_context=None

        for num in range(1,len_of_uploadedcsv_col):
            converted_num = str(num)
            fig=fig+converted_num
            em_list_fig_twolines.append(fig)

        for j in range(1,len(em_list_fig_twolines)):#len(em_list)   
            
            pdlineone= list(data_frame_bar[data_frame_col_names[0]])
            pdToList = list(data_frame_bar[data_frame_col_names[j]])        
            pdToList2 = []

            for i in pdToList:
                pdToList2.append(i+(i*0.1))

            trace0=go.Scatter(
                x=pdlineone,
                y=pdToList,
                mode='lines',            
            )

            trace1=go.Scatter(
                x=pdlineone,
                y=pdToList2,
                mode='lines',            
            )

            data=[trace0,trace1]
            layout=go.Layout()

            #fig=go.Figure(data=data,layout=layout)
            em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html()    

        #context_main={'key':em_list_fig_twolines}  
        # code for many line charts, with two lines ends here..........................
        #######################################################################################################
        #######chart1 function code pasted here ends here.....
        #######################################################################################################    
        context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'chart66':fig_bar_context,
        'column_header':column_header,'column_header2':column_header2,'data_frame_col_one':data_frame_col_names,
        'data_frame_col_one':data_frame_col_names,'em_list':em_list,'em_list_fig_twolines':em_list_fig_twolines,
        'selected_value_dropdown_cur':selected_value_dropdown_cur,'selected_value_dropdown_vol':selected_value_dropdown_vol,
        'list_radio':list_radio,'selected_value_dropdown_colmn':selected_value_dropdown_colmn,


        'dfr': tabular_form_context, "chart555": heat_fig_context,'chart66':fig_bar_context,
        'column_header':column_header,'data_frame_col_one':data_frame_col_names,
        'data_frame_col_one':data_frame_col_names,'em_list':em_list,  'dropdown_selected_bat_cur_convrt_string':dropdown_selected_bat_cur_convrt_string,
        'em_list_fig_twolines':em_list_fig_twolines,'notes':notes
        
        } 
        
        return render(request, 'chart1.html',context_main)        

        
    else:
        return render(request,'try2.html')



def chart2(request):
    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv   

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
    column_header2=list(scores.columns.values)

    
    heat_fig = px.imshow(scores,x=column_header,width=600, height=600)
    heat_fig_context = heat_fig.to_html()

    # code for heatmap  ends here -------------   

    ######
    # code for heatmap2 extra identification
    csv_obj_indent=Identification_model.objects.first()
    df_table_inden=csv_obj_indent.csv   

    csv_uploaded_iden = df_table_inden   

    df_iden = ad.abstraction.data.load_dataset(csv_uploaded_iden)
    tabular_form_context=df.to_html()     
    
    steps = 2000
    scores_iden = ad.abstraction.correlations.dtw_correlations(df_iden, csv_uploaded, steps) 
    scores_iden = (scores_iden - 1) *(-1)
    
    column_header_iden=list(scores_iden.columns.values)
    
    heat_fig_iden = px.imshow(scores_iden,x=column_header_iden,width=600, height=600)
    heat_fig_context_Iden= heat_fig_iden.to_html()
    # code for heatmap 2 exta identification ends here -------------  
    ######

    #####
    #code for bar chart exta identification.....  
    
    fig_bar_iden = px.bar(            
        data_frame = scores_iden['AccY (g)'],         
        
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
    fig_bar_iden.update_yaxes(visible=False)
    fig_bar_iden.update_xaxes(visible=False)
    fig_bar_context_iden = fig_bar_iden.to_html()

    #code for bar chart extra identification ends here-----------------
    #####


    # code for radio button yes no in data check
    #selected dropdown code 
    # dropdown one
    temp2=text.objects.filter(id=14).values('battery_current')
    answers_list = list(temp2)
    finaloption=answers_list[0]
    selected_value_dropdown_cur=finaloption.get("battery_current")

    temp3=text.objects.filter(id=14).values('battery_voltage')
    answers_list_3 = list(temp3)
    finaloption_3=answers_list_3[0]
    selected_value_dropdown_vol=finaloption_3.get("battery_voltage")

    list_radio = ["no", "yes"]
    temp4=text.objects.filter(id=14).values('remove_first_col')
    answers_list_4 = list(temp4)
    finaloption_4=answers_list_4[0]
    selected_value_dropdown_colmn=finaloption_4.get("remove_first_col") 
    # code for radio button yes no in data check......
    #selected dropdown code  ends here.... ...............................................................

    #code for bar chart
    
    # csv_obj_csvbar=Csv_for_heat.objects.first()
    # Csv_for_heat.objects.first()
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    data_frame_col_names=list(df.columns.values)
    
    
    fig_bar = px.bar(            
        data_frame = scores['AccY (g)'],         
        
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
    fig_bar.update_yaxes(visible=False)
    fig_bar.update_xaxes(visible=False)
    fig_bar_context = fig_bar.to_html()

    #code for bar chart ends here-----------------

    #code for several line charts

    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list=[]    
    figures={}
    fig='fig'
    ele_context=None

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list.append(fig)

    for j in range(1,len(em_list)):#len(em_list)
        em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()

    #code for several line charts end here.....

    # code for many line charts, with two lines
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv    
    
    csv_uploaded = df_table_data    
    
    df = ad.abstraction.data.load_dataset(csv_uploaded) 
    data_frame_col_names=list(df.columns.values)
    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list_fig_twolines=[]    
    figures={}
    fig='fig'
    ele_context=None

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list_fig_twolines.append(fig)

    for j in range(1,len(em_list_fig_twolines)):#len(em_list)   
        
        pdlineone= list(data_frame_bar[data_frame_col_names[0]])
        pdToList = list(data_frame_bar[data_frame_col_names[j]])        
        pdToList2 = []

        for i in pdToList:
            pdToList2.append(i+(i*0.1))

        trace0=go.Scatter(
            x=pdlineone,
            y=pdToList,
            mode='lines',            
        )

        trace1=go.Scatter(
            x=pdlineone,
            y=pdToList2,
            mode='lines',            
        )

        data=[trace0,trace1]
        layout=go.Layout(title='Average Home Goals by Year')

        #fig=go.Figure(data=data,layout=layout)
        em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html()    

    #context_main={'key':em_list_fig_twolines}  
    # code for many line charts, with two lines ends here..........................

    context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'heat_fig_context_Iden':heat_fig_context_Iden,'chart66':fig_bar_context,'fig_bar_context_iden':fig_bar_context_iden,
    'column_header':column_header,'column_header2':column_header2,'data_frame_col_one':data_frame_col_names,
    'data_frame_col_one':data_frame_col_names,'em_list':em_list,'em_list_fig_twolines':em_list_fig_twolines,
    'selected_value_dropdown_cur':selected_value_dropdown_cur,'selected_value_dropdown_vol':selected_value_dropdown_vol,
    'list_radio':list_radio,'selected_value_dropdown_colmn':selected_value_dropdown_colmn
    
    } 
    
    return render(request, 'try2.html',context_main)
    









def chart1(request):#ds_one home url function view    

    # code to select csv from models
    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv   

    #comman_datafrme_without_process= pd.read_csv(df_table_data)
    
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
    
    heat_fig = px.imshow(scores,x=column_header,width=600, height=600)
    heat_fig_context = heat_fig.to_html()

    # code for heatmap  ends here -------------




    # code to save csv scores in Csv_score model -------------
    # info = pd.DataFrame(scores) 
    x=scores.to_csv(encoding='utf-8', index=False)

    temp_query=Csv_score_downld.objects.filter(id=1)

    if temp_query:
        Csv_score_downld.objects.filter(id=1).update(csv=x,id=1)
    else:
        c = Csv_score_downld(csv=x,id=1)
        c.save()
    
    notes=Csv_score_downld.objects.all()

    # code to save csv scores in Csv_score model__ ends here -------------

    

    #code for bar chart   
    
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    data_frame_col_names=list(df.columns.values)
    # dropdown_selected_bat_cur_convrt_string=None
    #custom bar chart saved from bat_cur dropdown code
    # obj_text_model=text.objects.first()
    # if obj_text_model:
    #     dropdown_selected_bat_cur=obj_text_model.battery_current    
    #     dropdown_selected_bat_cur_convrt_string=str(dropdown_selected_bat_cur)

    # if dropdown_selected_bat_cur_convrt_string == None:
    #     dropdown_selected_bat_cur_convrt_string = data_frame_col_names[1]
    
    dropdown_selected_bat_cur_convrt_string = data_frame_col_names[1]
      
    
    fig_bar = px.bar(            
    data_frame = scores[dropdown_selected_bat_cur_convrt_string],         
    
    # opacity = 0.9,
    orientation = "v",
    barmode = 'group',
    title='',
    )
    fig_bar.update_yaxes(visible=False)
    fig_bar.update_layout(showlegend=False)

    fig_bar_context = fig_bar.to_html()
    ###################################

    #code for bar chart ends here-----------------

    #code for several line charts

    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list=[]    
    figures={}
    fig='fig'
    ele_context=None

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list.append(fig)

    for j in range(1,len(em_list)):#len(em_list)
        em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()

    #code for several line charts end here.....


    # code for many line charts, with two lines
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv    
    
    csv_uploaded = df_table_data    
    
    df = ad.abstraction.data.load_dataset(csv_uploaded) 
    data_frame_col_names=list(df.columns.values)
    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list_fig_twolines=[]    
    figures={}
    fig='fig'
    ele_context=None

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list_fig_twolines.append(fig)

    for j in range(1,len(em_list_fig_twolines)):#len(em_list)   
        
        pdlineone= list(data_frame_bar[data_frame_col_names[0]])
        pdToList = list(data_frame_bar[data_frame_col_names[j]])        
        pdToList2 = []

        for i in pdToList:
            pdToList2.append(i+(i*0.1))

        trace0=go.Scatter(
            x=pdlineone,
            y=pdToList,
            mode='lines',            
        )

        trace1=go.Scatter(
            x=pdlineone,
            y=pdToList2,
            mode='lines',            
        )

        data=[trace0,trace1]
        layout=go.Layout()

        #fig=go.Figure(data=data,layout=layout)
        em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html()    

    #context_main={'key':em_list_fig_twolines}  
    # code for many line charts, with two lines ends here..........................

    

    
    
    context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'chart66':fig_bar_context,
    'column_header':column_header,'data_frame_col_one':data_frame_col_names,
    'data_frame_col_one':data_frame_col_names,'em_list':em_list,  'dropdown_selected_bat_cur_convrt_string':dropdown_selected_bat_cur_convrt_string,
    'em_list_fig_twolines':em_list_fig_twolines,'notes':notes
    
    }     

    return render(request, 'chart1.html',context_main)


def venue(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=scores.csv'
    lines=[]
    venue= Csv_score_downld.objects.all()

    for item in venue:
        lines.append(f'{item.csv}\n')



    # lines=["this is line 1 \n",
    # "this is line 2 \n",
    # "this is line 3 \n"]
    response.writelines(lines)
    return response


def iden(request):#ds_one home url function view    

    # code to select csv from models
    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv   

    #comman_datafrme_without_process= pd.read_csv(df_table_data)
    
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
    
    heat_fig = px.imshow(scores,x=column_header,width=600, height=600)
    heat_fig_context = heat_fig.to_html()

    # code for heatmap  ends here -------------   


    

    #code for bar chart   
    
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    data_frame_col_names=list(df.columns.values)

    #custom bar chart saved from bat_cur dropdown code
    obj_text_model=text.objects.first()
    dropdown_selected_bat_cur=obj_text_model.battery_current    
    dropdown_selected_bat_cur_convrt_string=str(dropdown_selected_bat_cur)

    if dropdown_selected_bat_cur_convrt_string == '0':
        dropdown_selected_bat_cur_convrt_string = data_frame_col_names[0]
    elif dropdown_selected_bat_cur_convrt_string == 'None':
        dropdown_selected_bat_cur_convrt_string = data_frame_col_names[0]

     
    
    fig_bar = px.bar(            
    data_frame = scores[dropdown_selected_bat_cur_convrt_string],         
    
    opacity = 0.9,
    orientation = "v",
    barmode = 'group',
    title='',
    )
    fig_bar.update_yaxes(visible=False)
    fig_bar.update_layout(showlegend=False)

    fig_bar_context = fig_bar.to_html()
    ###################################

    #code for bar chart ends here-----------------

    #code for several line charts

    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list=[]    
    figures={}
    fig='fig'
    ele_context=None

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list.append(fig)

    for j in range(1,len(em_list)):#len(em_list)
        em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()

    #code for several line charts end here.....


    # code for many line charts, with two lines
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv    
    
    csv_uploaded = df_table_data    
    
    df = ad.abstraction.data.load_dataset(csv_uploaded) 
    data_frame_col_names=list(df.columns.values)
    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list_fig_twolines=[]    
    figures={}
    fig='fig'
    ele_context=None

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list_fig_twolines.append(fig)

    for j in range(1,len(em_list_fig_twolines)):#len(em_list)   
        
        pdlineone= list(data_frame_bar[data_frame_col_names[0]])
        pdToList = list(data_frame_bar[data_frame_col_names[j]])        
        pdToList2 = []

        for i in pdToList:
            pdToList2.append(i+(i*0.1))

        trace0=go.Scatter(
            x=pdlineone,
            y=pdToList,
            mode='lines',            
        )

        trace1=go.Scatter(
            x=pdlineone,
            y=pdToList2,
            mode='lines',            
        )

        data=[trace0,trace1]
        layout=go.Layout()

        #fig=go.Figure(data=data,layout=layout)
        em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html()    

    #context_main={'key':em_list_fig_twolines}  
    # code for many line charts, with two lines ends here..........................

    

    
    
    context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'chart66':fig_bar_context,
    'column_header':column_header,'data_frame_col_one':data_frame_col_names,
    'data_frame_col_one':data_frame_col_names,'em_list':em_list,  'dropdown_selected_bat_cur_convrt_string':dropdown_selected_bat_cur_convrt_string,
    'em_list_fig_twolines':em_list_fig_twolines
    
    }     

    return render(request, 'chartsiden.html',context_main)



def watchdemo(r):
    return render (r,'watchdemo.html')

def sample2(request):    
    if request.method == 'POST':     
        text1=request.POST.get('text')
        no_of_operational=request.POST.get('no_of_operational')
        cut_off_thresold=request.POST.get('cut_off_thresold')        
        id=request.POST.get('id')  
        query= text.objects.filter(id=1)
        if query:
            text.objects.filter(id=1).update(text=text1,no_of_operational=no_of_operational,cut_off_thresold=cut_off_thresold,id=id)
        else:
            b = text(text=text1,no_of_operational=no_of_operational,cut_off_thresold=cut_off_thresold,id=id)
            b.save()
    
        
        # def chart() resources copied from above function-starts

        # code for selecting csv from models
        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv
        
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

        # dropdown code 
        csv_obj_csvbar=Csv_for_heat.objects.first()
        csv_bar_file=csv_obj_csvbar.csv 
        csv_bar_file_two_readcsv = read_csv(csv_bar_file)

        obj_text_model=text.objects.first()# dropdown code
        text_file_selected_dropdown=obj_text_model.text        
        text_file_selected_dropdown_convrt_string=str(text_file_selected_dropdown)# dropdown code ends

        #code for dropdown parameter saved in the model named text, to be retrived as a label above bar chart
        obj_para=text.objects.first()
        label_shown=obj_para.text 
        
        #code for dropdown parameter saved in the model named text, to be retrived as a label above bar chart...ends here

        # bar chart code 
        data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)
        data_frame_col_one=list(data_frame_bar.columns.values)#list of first column , not used presently
        
        fig_bar = px.bar(            
        data_frame = scores[text_file_selected_dropdown_convrt_string],         
        
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
        fig_bar.update_yaxes(visible=False)
        fig_bar.update_layout(showlegend=False)

        fig_bar_context = fig_bar.to_html()
        # bar chart code ends here---------

        # def chart() resources copied from avove function-ends....

        #code for several line charts
        data_frame_col_names=list(df.columns.values)
        len_of_uploadedcsv_col=len(data_frame_col_names)

        em_list=[]    
        figures={}
        fig='fig'
        ele_context=None

        for num in range(1,len_of_uploadedcsv_col):
            converted_num = str(num)
            fig=fig+converted_num
            em_list.append(fig)

        for j in range(1,len(em_list)):#len(em_list)
            em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()




        #code for several line charts end here.....

        # code for many line charts, with two lines
        csv_obj_csvbar=Csv_for_heat.objects.first()
        csv_bar_file=csv_obj_csvbar.csv  
        csv_bar_file_two_readcsv = read_csv(csv_bar_file)
        data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv    
        
        csv_uploaded = df_table_data    
        
        df = ad.abstraction.data.load_dataset(csv_uploaded) 
        data_frame_col_names=list(df.columns.values)
        len_of_uploadedcsv_col=len(data_frame_col_names)

        em_list_fig_twolines=[]    
        figures={}
        fig='fig'
        ele_context=None

        for num in range(1,len_of_uploadedcsv_col):
            converted_num = str(num)
            fig=fig+converted_num
            em_list_fig_twolines.append(fig)

        for j in range(1,len(em_list_fig_twolines)):#len(em_list)   
            
            pdlineone= list(data_frame_bar[data_frame_col_names[0]])
            pdToList = list(data_frame_bar[data_frame_col_names[j]])        
            pdToList2 = []

            for i in pdToList:
                pdToList2.append(i+(i*0.1))

            trace0=go.Scatter(
                x=pdlineone,
                y=pdToList,
                mode='lines',            
            )

            trace1=go.Scatter(
                x=pdlineone,
                y=pdToList2,
                mode='lines',            
            )

            data=[trace0,trace1]
            layout=go.Layout(title='Average Home Goals by Year')

            #fig=go.Figure(data=data,layout=layout)
            em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html()    

        #context_main={'key':em_list_fig_twolines}  
        # code for many line charts, with two lines ends here..........................
        
        
        return render(request,'heatmap3.html',{'dfr': tabular_form_context, "chart555": heat_fig_context,'chart66':fig_bar_context,'column_header':column_header,'label_shown':label_shown,'em_list':em_list,'em_list_fig_twolines':em_list_fig_twolines})
    
    else:
        return render(request,'heatmap3.html')
    




    





def sample3(request):
    if request.method == 'POST':
        if request.POST.get('text'):
            savevalue=text()
            savevalue.text=request.POST.get('text')
            savevalue.no_of_operational=request.POST.get('no_of_operational')
            savevalue.cut_off_thresold=request.POST.get('cut_off_thresold')
            # savevalue.battery_voltage=request.POST.get('bat_vol')
            # savevalue.battery_current=request.POST.get('bat_cur')
            # savevalue.remove_first_col=request.POST.get('remove_fir_col')

            savevalue.id=request.POST.get('id')
            savevalue.save()

            # def chart() resources copied from above function-starts


            # code for selecting csv from models
            csv_obj_csvheat=Csv_for_heat.objects.first()
            df_table_data=csv_obj_csvheat.csv
            
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

            # dropdown code 
            csv_obj_csvbar=Csv_for_heat.objects.first()
            csv_bar_file=csv_obj_csvbar.csv 
            csv_bar_file_two_readcsv = read_csv(csv_bar_file)

            obj_text_model=text.objects.first()# dropdown code
            text_file_selected_dropdown=obj_text_model.text
            
            text_file_selected_dropdown_convrt_string=str(text_file_selected_dropdown)# dropdown code ends

            #code for dropdown parameter saved in the model named text, to be retrived as a label above bar chart
            obj_para=text.objects.first()
            label_shown=obj_para.text 
            
            #code for dropdown parameter saved in the model named text, to be retrived as a label above bar chart...ends here

            data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)
            data_frame_col_one=list(data_frame_bar.columns.values)#list of first column , not used presently
            
            fig_bar = px.bar(            
            data_frame = scores[text_file_selected_dropdown_convrt_string],         
           
            opacity = 0.9,
            orientation = "v",
            barmode = 'group',
            title='',
            )
            fig_bar.update_yaxes(visible=False)
            fig_bar.update_layout(showlegend=False)

            fig_bar_context = fig_bar.to_html()
            # bar chart code ends here---------

            # def chart() resources copied from avove function-ends




            #code for several line charts
            data_frame_col_names=list(df.columns.values)
            len_of_uploadedcsv_col=len(data_frame_col_names)

            em_list=[]    
            figures={}
            fig='fig'
            ele_context=None

            for num in range(1,len_of_uploadedcsv_col):
                converted_num = str(num)
                fig=fig+converted_num
                em_list.append(fig)

            for j in range(1,len(em_list)):#len(em_list)
                em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()




            #code for several line charts end here.....
            
            
            return render(request,'heatmap3.html',{'dfr': tabular_form_context, "chart555": heat_fig_context,'chart66':fig_bar_context,'column_header':column_header,'label_shown':label_shown,'em_list':em_list})
        
        else:
            return render(request,'heatmap3.html')
    else:
            return render(request,'heatmap3.html')






def try2(request):#ds_one home url function view 
    
    # code to select csv from models
    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv   

    #comman_datafrme_without_process= pd.read_csv(df_table_data)
    
            
    
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
    
    heat_fig = px.imshow(scores,x=column_header,width=600, height=600)
    heat_fig_context = heat_fig.to_html()

    # code for heatmap  ends here -------------   

    #code for bar chart
    
    # csv_obj_csvbar=Csv_for_heat.objects.first()
    # Csv_for_heat.objects.first()
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

    data_frame_col_names=list(df.columns.values)
    
    
    fig_bar = px.bar(            
        data_frame = scores['AccY (g)'],         
        
        opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
    fig_bar.update_yaxes(visible=False)
    fig_bar.update_xaxes(visible=False)
    fig_bar_context = fig_bar.to_html()

    #code for bar chart ends here-----------------

    #code for several line charts

    len_of_uploadedcsv_col=len(data_frame_col_names)

    em_list=[]    
    figures={}
    fig='fig'
    ele_context=None

    for num in range(1,len_of_uploadedcsv_col):
        converted_num = str(num)
        fig=fig+converted_num
        em_list.append(fig)

    for j in range(1,3):#len(em_list)
        em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j],height=500,width=1200,).to_html()




    #code for several line charts end here.....

    
    
    context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'chart66':fig_bar_context,
    'column_header':column_header,'data_frame_col_one':data_frame_col_names,
    'data_frame_col_one':data_frame_col_names,'em_list':em_list,
    
    
    
    } 
    

    
    return render(request, 'try2.html',context_main)
    
    





    







    


  








