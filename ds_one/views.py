from asyncio.windows_events import NULL
from operator import is_not, le
from django.http import JsonResponse , HttpResponse
from django.shortcuts import render , HttpResponse
import plotly.express as px
from core.models import  Csv_for_heat , Csv_for_heat , text , Identification_model , Csv_score_downld , inject_anamolies 
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
# sys.path.append('C:\\Users\\pankaj\\Desktop\\GTC running app files\\new_11-10-2022\\django-plotly-integration\\ds_one')
sys.path.append('C:\\Users\\pankaj\\Desktop\\GTC running app files\\git clone 2 copy\\django-plotly-integration\\ds_one')

import Aradiss as ad
# from .Aradiss.abstraction import data
# from .Aradiss.abstraction import correlations
path = os.getcwd()

import ds_one.dash
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.figure_factory as ff

from io import StringIO
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


from django.http import HttpResponse







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
                        
        #code to select csv from models ends here-------

        # code to convert csv data to tabular form 
        csv_uploaded = df_table_data   # ref line no 40__This should point to the csv file you upload 

        df = ad.abstraction.data.load_dataset(csv_uploaded)
        tabular_form_context=df.to_html()
        # code to convert csv data to tabular form ends here ------

        ######dropdown current & voltage
        ###########################################################
        steps = 2000
        scores = ad.abstraction.correlations.dtw_correlations(df, csv_uploaded, steps) 
        scores = (scores - 1) *(-1)
        
        column_header=list(scores.columns.values)
        column_header2=list(scores.columns.values)
        ######dropdown current & voltage...........ends............
        ###########################################################

        #############################################
        ###################drop down code############
        
        temp2=text.objects.filter(id=1).values('text')
        answers_list = list(temp2)
        finaloption=answers_list[0]
        selected_value_dropdown_cur=finaloption.get("text")

        list_radio = ["no", "yes"]
        temp4=text.objects.filter(id=1).values('remove_first_col')
        answers_list_4 = list(temp4)
        finaloption_4=answers_list_4[0]
        selected_value_remove_first_col=finaloption_4.get("remove_first_col")

        #############################################
        ###################drop down code############...ends
        

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

        chart2='yes_for_step1'

        context_main={'dfr': tabular_form_context,'list_radio':list_radio,
        'column_header':column_header,'column_header2':column_header2,
        'selected_value_remove_first_col':selected_value_remove_first_col,       
        'chart2':chart2,
        'selected_value_dropdown4':selected_value_dropdown4,} 

        return render(request, 'try2.html',context_main)
        # except:
        #     return HttpResponse('havent uploaded anything, please go back and upload file')    
       
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

            pdToList2=[x+(x * 0.1) for x in pdToList]# every element multiplied by 10%

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




universal_list=[]

def chartdetection(request):  
    if request.method == 'POST':     
        num_received=request.POST.get('num_sent')
    
    step = 1

    # code for taking out data in csv stored in model 
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)
    # code for taking out data in csv stored in model 

    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv 
    csv_uploaded = df_table_data   
    
    # code for making making dataframe for line chart
    df = ad.abstraction.data.load_dataset(csv_uploaded) 
    data_frame_col_names=list(df.columns.values)
    len_of_uploadedcsv_col=len(data_frame_col_names)
    # code for making making dataframe for line chart

        
    if len_of_uploadedcsv_col <5:#  this code will work if length of csv coulmn are less than 5
        em_list_fig_twolines=[]    
        fig='fig'
        
        for num in range(1,len_of_uploadedcsv_col):#code for making a list of lenght matching to <5 figures
            converted_num = str(num)
            fig=fig+converted_num
            em_list_fig_twolines.append(fig)   
            

        for j in range(1,len_of_uploadedcsv_col): 
            pdlineone= list(data_frame_bar[data_frame_col_names[0]]) # for line 1
            pdToList = list(data_frame_bar[data_frame_col_names[j]]) # for line 2       
            pdToList2 = []

            pdToList2=[x+(x * 0.1) for x in pdToList]# every element multiplied by 10%

            original=go.Scatter(
                x=pdlineone,
                y=pdToList,
                mode='lines',            
            )

            Ten_percent_deviation=go.Scatter(
                x=pdlineone,
                y=pdToList2,
                mode='lines',           
            )

            data=[original,Ten_percent_deviation]
            layout=go.Layout(title='', height=310, width=1800,showlegend=False)
        
            em_list_fig_twolines[j-1]=fig=go.Figure(data=data,layout=layout).to_html()#all figures stored in list  
        # code for many line charts, with two lines ends here..........................  
        context_main={
        'data_frame_col_one':data_frame_col_names,
        'data_frame_col_one':data_frame_col_names,'em_list_fig_twolines':em_list_fig_twolines,  'step':step , 
        'len_of_uploadedcsv_col':len_of_uploadedcsv_col ,'data_frame_col_names':data_frame_col_names
        
        }         
        return render(request, 'chartsdetection.html',context_main)
    elif len_of_uploadedcsv_col >=5:#  this code will work if length of csv coulmn is more than 5 and less than 9
        em_list_fig_twolines=[]       
        figures={}
        fig='fig'
        ele_context=None
        for num in range(1,5):
            converted_num = str(num)
            fig=fig+converted_num
            em_list_fig_twolines.append(fig)              

        for j in range(0,6-2):
            pdlineone= list(data_frame_bar[data_frame_col_names[0]])
            pdToList = list(data_frame_bar[data_frame_col_names[j+1]])        
            pdToList2 = []
            pdToList2=[x+(x * 0.1) for x in pdToList]# every element multiplied by 10%

            original=go.Scatter(
                x=pdlineone,
                y=pdToList,
                mode='lines',            
            )
            Ten_percent_deviation=go.Scatter(
                x=pdlineone,
                y=pdToList2,
                mode='lines',            
            )
            data=[original,Ten_percent_deviation]
            title_name=data_frame_col_names[j+1]
            layout=go.Layout(title=title_name, height=310, width=1800,showlegend=False)        
            em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html() #all figures stored in list     
        # code for many line charts, with two lines ends here.......................... 
        context_main={
        'data_frame_col_one':data_frame_col_names,
        'data_frame_col_one':data_frame_col_names,'em_list_fig_twolines':em_list_fig_twolines,  'step':step , 
        'len_of_uploadedcsv_col':len_of_uploadedcsv_col , 'data_frame_col_names':data_frame_col_names        
        }         
        return render(request, 'chartsdetection.html',context_main)



def chartdetection2(request): 
    # code for taking out data in csv stored in model 
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)
    # code for taking out data in csv stored in model 

    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv 
    csv_uploaded = df_table_data   
    
    # code for making making dataframe for line chart
    df = ad.abstraction.data.load_dataset(csv_uploaded) 
    data_frame_col_names=list(df.columns.values)
    len_of_uploadedcsv_col=len(data_frame_col_names)
    # code for making making dataframe for line chart

    universal_list.append(5)

    val=sum(universal_list)   


    if val>len_of_uploadedcsv_col:
        universal_list.clear()
        val=sum(universal_list)
        return HttpResponse('Nothing to show please go back') 

    if val==len_of_uploadedcsv_col:
        em_list_fig_twolines=[1]    
        
        fig='fig' 

        step2=2
        step=0 

        var=0
         
        pdlineone= list(data_frame_bar[data_frame_col_names[0]]) # for line 1
        pdToList = list(data_frame_bar[data_frame_col_names[-1]]) # for line 2       
        pdToList2 = []
        var+=1

        pdToList2=[x+(x * 0.1) for x in pdToList]# every element multiplied by 10%

        original=go.Scatter(
            x=pdlineone,
            y=pdToList,
            mode='lines',            
        )

        Ten_percent_deviation=go.Scatter(
            x=pdlineone,
            y=pdToList2,
            mode='lines',           
        )

        data=[original,Ten_percent_deviation]
        title_name=data_frame_col_names[-1]
        layout=go.Layout(title=title_name, height=310, width=1800,showlegend=False)
    
        em_list_fig_twolines[0]=fig=go.Figure(data=data,layout=layout).to_html()#all figures stored in list 
        # code for many line charts, with two lines ends here..........................  
        context_main={
        'data_frame_col_one':data_frame_col_names,
        'data_frame_col_one':data_frame_col_names,'em_list_fig_twolines':em_list_fig_twolines,  
        'len_of_uploadedcsv_col':len_of_uploadedcsv_col ,'data_frame_col_names':data_frame_col_names,
        'val':val,'step2':step2, 'step':step
        
        }         
        return render(request, 'chartsdetection.html',context_main)

    else:      

        em_list_fig_twolines=[]  
        step2=2  
        step = 1          
        fig='fig'                

        for num in range(val,val+6):#code for making a list of lenght matching to <5 figures
            converted_num = str(num)
            fig=fig+converted_num
            em_list_fig_twolines.append(fig)   
            
        var=0
        for j in range(val,val+6): 
            pdlineone= list(data_frame_bar[data_frame_col_names[0]]) # for line 1
            pdToList = list(data_frame_bar[data_frame_col_names[j-2]]) # for line 2       
            pdToList2 = []
            var+=1

            pdToList2=[x+(x * 0.1) for x in pdToList]# every element multiplied by 10%

            original=go.Scatter(
                x=pdlineone,
                y=pdToList,
                mode='lines',            
            )

            Ten_percent_deviation=go.Scatter(
                x=pdlineone,
                y=pdToList2,
                mode='lines',           
            )

            data=[original,Ten_percent_deviation]
     
            title_name=data_frame_col_names[j-2]
            layout=go.Layout(title=title_name, height=310, width=1800,showlegend=False)
        
            em_list_fig_twolines[var-1]=fig=go.Figure(data=data,layout=layout).to_html()#all figures stored in list  
        # code for many line charts, with two lines ends here..........................  
        context_main={
        'data_frame_col_one':data_frame_col_names,
        'data_frame_col_one':data_frame_col_names,'em_list_fig_twolines':em_list_fig_twolines,  
        'len_of_uploadedcsv_col':len_of_uploadedcsv_col ,'data_frame_col_names':data_frame_col_names,
        'val':val,'step2':step2, 'list':universal_list,'step':step
        }         
        return render(request, 'chartsdetection.html',context_main)


def chartdetection3(request): 
    # code for taking out data in csv stored in model 
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)
    # code for taking out data in csv stored in model 

    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv 
    csv_uploaded = df_table_data   
    
    # code for making making dataframe for line chart
    df = ad.abstraction.data.load_dataset(csv_uploaded) 
    data_frame_col_names=list(df.columns.values)
    len_of_uploadedcsv_col=len(data_frame_col_names)
    # code for making making dataframe for line chart

    if sum(universal_list) == 5:
        universal_list.pop()
        em_list_fig_twolines=[]       
        figures={}  
        step=1     
        if not universal_list:
            step2=10
        else:
            step2=2
        fig='fig'
        ele_context=None
        for num in range(1,5):
            converted_num = str(num)
            fig=fig+converted_num
            em_list_fig_twolines.append(fig)              

        for j in range(0,6-2):
            pdlineone= list(data_frame_bar[data_frame_col_names[0]])
            pdToList = list(data_frame_bar[data_frame_col_names[j+1]])        
            pdToList2 = []
            pdToList2=[x+(x * 0.1) for x in pdToList]# every element multiplied by 10%

            original=go.Scatter(
                x=pdlineone,
                y=pdToList,
                mode='lines',            
            )
            Ten_percent_deviation=go.Scatter(
                x=pdlineone,
                y=pdToList2,
                mode='lines',            
            )
            data=[original,Ten_percent_deviation]
            title_name=data_frame_col_names[j+1]
            layout=go.Layout(title=title_name, height=310, width=1800,showlegend=False)        
            em_list_fig_twolines[j]=fig=go.Figure(data=data,layout=layout).to_html() #all figures stored in list               
        # code for many line charts, with two lines ends here.......................... 
        context_main={
        'data_frame_col_one':data_frame_col_names,
        'data_frame_col_one':data_frame_col_names,'em_list_fig_twolines':em_list_fig_twolines,  'step2':step2 , 'step':step,
        'len_of_uploadedcsv_col':len_of_uploadedcsv_col , 'data_frame_col_names':data_frame_col_names        
        }         
        return render(request, 'chartsdetection.html',context_main)  

    elif sum(universal_list) > 5:   
        universal_list.pop()
        val=sum(universal_list)
        em_list_fig_twolines=[]  
        step=1

        if not universal_list:
            step2=10
        else:
            step2=2    
        
        fig='fig'                

        for num in range(val,val+6):#code for making a list of lenght matching to <5 figures
            converted_num = str(num)
            fig=fig+converted_num
            em_list_fig_twolines.append(fig)   
            
        var=0
        for j in range(val,val+6): 
            pdlineone= list(data_frame_bar[data_frame_col_names[0]]) # for line 1
            pdToList = list(data_frame_bar[data_frame_col_names[j-2]]) # for line 2       
            pdToList2 = []
            var+=1

            pdToList2=[x+(x * 0.1) for x in pdToList]# every element multiplied by 10%

            original=go.Scatter(
                x=pdlineone,
                y=pdToList,
                mode='lines',            
            )

            Ten_percent_deviation=go.Scatter(
                x=pdlineone,
                y=pdToList2,
                mode='lines',           
            )

            data=[original,Ten_percent_deviation]
     
            title_name=data_frame_col_names[j-2]
            layout=go.Layout(title=title_name, height=310, width=1800,showlegend=False)
        
            em_list_fig_twolines[var-1]=fig=go.Figure(data=data,layout=layout).to_html()#all figures stored in list              
        # code for many line charts, with two lines ends here..........................  
        context_main={
        'data_frame_col_one':data_frame_col_names,
        'data_frame_col_one':data_frame_col_names,'em_list_fig_twolines':em_list_fig_twolines,  
        'len_of_uploadedcsv_col':len_of_uploadedcsv_col ,'data_frame_col_names':data_frame_col_names,
        'val':val,'step2':step2 , 'list':universal_list, 'step':step
        
        }         
        return render(request, 'chartsdetection.html',context_main)

        


universal_list2=[]


def chartdetection_mlper(request):  
    if request.method == 'POST':     
        num_received=request.POST.get('num_sent')

    # code for taking out data in csv stored in model 
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)
    # code for taking out data in csv stored in model 

    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv 
    csv_uploaded = df_table_data   
    
    # code for making making dataframe for line chart
    df = ad.abstraction.data.load_dataset(csv_uploaded) 
    data_frame_col_names=list(df.columns.values)
    len_of_uploadedcsv_col=len(data_frame_col_names)
    # code for making making dataframe for line chart

    step=1
    only_for_step1=1

        
    if len_of_uploadedcsv_col <5:#  this code will work if length of csv coulmn are less than 5
        em_list=[]  
        emlistscatter=[]  
        fig='fig'

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
            title='Mean Percentage Error'
            )    
        fig_bar_context_b = fig_bar1.to_html()
        ##########################barchart for ML Performanve tab bar chart......ends#####
        ##################################################################################

        for num in range(1,len_of_uploadedcsv_col):#code for making a list of lenght matching to <5 figures
            converted_num = str(num)
            fig=fig+converted_num
            em_list.append(fig)   

        for num in range(1,len_of_uploadedcsv_col):
            converted_num = str(num)
            fig=fig+converted_num
            emlistscatter.append(fig)

        
        for j in range(0,len_of_uploadedcsv_col):#len(em_list)
            em_list[j-1]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j], height=310, width=1800,).to_html()

        for j in range(1,len_of_uploadedcsv_col):
            emlistscatter[j-1]=px.scatter(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j], height=310, width=310,).to_html()           

        
        # ..........................  
        context_main={
        'em_list':em_list,
        'emlistscatter':emlistscatter,    
        'fig_bar_context_b':fig_bar_context_b,  'step':step  
        } 
        return render(request, 'chartsdetection_ml_perform.html',context_main)
    elif len_of_uploadedcsv_col >=5:#  this code will work if length of csv coulmn is more than 5 and less than 9
        em_list=[]  
        emlistscatter=[]  
        fig='fig'

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
            title='Mean Percentage Error'
            )    
        fig_bar_context_b = fig_bar1.to_html()
        ##########################barchart for ML Performanve tab bar chart......ends#####
        ##################################################################################
        
        for num in range(1,5):
            converted_num = str(num)
            fig=fig+converted_num
            em_list.append(fig)        

        for num in range(1,5):
            converted_num = str(num)
            fig=fig+converted_num
            emlistscatter.append(fig)  

        for j in range(0,6-2):#len(em_list)
            em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j+1], height=310, width=1800,).to_html()

        for j in range(0,6-2):
            emlistscatter[j]=px.scatter(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j+1], height=310, width=310,).to_html()     
        
        context_main={
        'em_list':em_list,
        'emlistscatter':emlistscatter,    
        'fig_bar_context_b':fig_bar_context_b, 'step':step   , 'only_for_step1':only_for_step1
        } 
        return render(request, 'chartsdetection_ml_perform.html',context_main)



def chartdetection_mlper2(request):
    # code for taking out data in csv stored in model 
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)
    # code for taking out data in csv stored in model 

    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv 
    csv_uploaded = df_table_data   
    
    # code for making making dataframe for line chart
    df = ad.abstraction.data.load_dataset(csv_uploaded) 
    data_frame_col_names=list(df.columns.values)
    len_of_uploadedcsv_col=len(data_frame_col_names)
    # code for making making dataframe for line chart

    only_for_step1=2
    step=0

    universal_list2.append(5)

    val=sum(universal_list2)   


    if val>len_of_uploadedcsv_col:
        universal_list.clear()
        val=sum(universal_list)
        return HttpResponse('Nothing to show please go back') 

    if val==len_of_uploadedcsv_col:

        em_list=[1]  
        emlistscatter=[1]  
        fig='fig'
        step2=2
        step=5

        only_for_step1=3

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
            title='Mean Percentage Error'
            )    
        fig_bar_context_b = fig_bar1.to_html()
        ##########################barchart for ML Performanve tab bar chart......ends#####
        ##################################################################################
                 
        
        em_list[0]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[-1], height=310, width=1800,).to_html()
        
        emlistscatter[0]=px.scatter(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[-1], height=310, width=310,).to_html()  

        # code for many line charts, with two lines ends here..........................  
        context_main={
        'em_list':em_list,
        'emlistscatter':emlistscatter,    
        'fig_bar_context_b':fig_bar_context_b, 'step':step ,'only_for_step1':only_for_step1 , 'step2':step2
        
        }         
        return render(request, 'chartsdetection_ml_perform.html',context_main)      


    else: 
        em_list=[]  
        emlistscatter=[]  
        fig='fig'

        step=1
        step2=2

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
            title='Mean Percentage Error'
            )    
        fig_bar_context_b = fig_bar1.to_html()
        ##########################barchart for ML Performanve tab bar chart......ends#####
        ##################################################################################
        
        for num in range(val,val+6):
            converted_num = str(num)
            fig=fig+converted_num
            em_list.append(fig)        

        for num in range(val,val+6):
            converted_num = str(num)
            fig=fig+converted_num
            emlistscatter.append(fig)  

        var=0
        for j in range(val,val+6):#len(em_list)
            var+=1
            em_list[var-1]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j-2], height=310, width=1800,).to_html()
        var=0
        for j in range(val,val+6):
            var+=1
            emlistscatter[var-1]=px.scatter(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j-2], height=310, width=310,).to_html()     
        
        context_main={
        'em_list':em_list,
        'emlistscatter':emlistscatter,    
        'fig_bar_context_b':fig_bar_context_b, 'step':step   ,'only_for_step1':only_for_step1 , 'step2':step2
        } 
        return render(request, 'chartsdetection_ml_perform.html',context_main)



def chartdetection_mlper3(request): 
    # code for taking out data in csv stored in model 
    csv_obj_csvbar=Csv_for_heat.objects.first()
    csv_bar_file=csv_obj_csvbar.csv  
    csv_bar_file_two_readcsv = read_csv(csv_bar_file)
    data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)
    # code for taking out data in csv stored in model 

    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv 
    csv_uploaded = df_table_data   
    
    # code for making making dataframe for line chart
    df = ad.abstraction.data.load_dataset(csv_uploaded) 
    data_frame_col_names=list(df.columns.values)
    len_of_uploadedcsv_col=len(data_frame_col_names)
    # code for making making dataframe for line chart

    only_for_step1=2

    if sum(universal_list2) == 5:
        universal_list2.pop()

        if not universal_list2:
            step2=10
        else:
            step2=5

        step=1

        only_for_step1=1

        em_list=[]  
        emlistscatter=[]  
        fig='fig'

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
            title='Mean Percentage Error'
            )    
        fig_bar_context_b = fig_bar1.to_html()
        ##########################barchart for ML Performanve tab bar chart......ends#####
        ##################################################################################
        
        for num in range(1,5):
            converted_num = str(num)
            fig=fig+converted_num
            em_list.append(fig)        

        for num in range(1,5):
            converted_num = str(num)
            fig=fig+converted_num
            emlistscatter.append(fig)  

        for j in range(0,6-2):#len(em_list)
            em_list[j]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j+1], height=310, width=1800,).to_html()

        for j in range(0,6-2):
            emlistscatter[j]=px.scatter(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j+1], height=310, width=310,).to_html()     
        
        context_main={
        'em_list':em_list,
        'emlistscatter':emlistscatter,    
        'fig_bar_context_b':fig_bar_context_b, 'step':step , 'step2':step2 , 'only_for_step1':only_for_step1
        } 
        return render(request, 'chartsdetection_ml_perform.html',context_main)  

    elif sum(universal_list2) > 5:     
        universal_list2.pop()
        val=sum(universal_list2)        

        if not universal_list2:
            step2=10
        else:
            step2=2

        step=1  
        
        em_list=[]  
        emlistscatter=[]  
        fig='fig'

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
            title='Mean Percentage Error'
            )    
        fig_bar_context_b = fig_bar1.to_html()
        ##########################barchart for ML Performanve tab bar chart......ends#####
        ##################################################################################
        
        for num in range(val,val+6):
            converted_num = str(num)
            fig=fig+converted_num
            em_list.append(fig)        

        for num in range(val,val+6):
            converted_num = str(num)
            fig=fig+converted_num
            emlistscatter.append(fig)  

        var=0
        for j in range(val,val+6):#len(em_list)
            var+=1
            em_list[var-1]=px.line(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j-2], height=310, width=1800,).to_html()
        var=0
        for j in range(val,val+6):
            var+=1
            emlistscatter[var-1]=px.scatter(data_frame_bar,x=data_frame_col_names[0], y=data_frame_col_names[j-2], height=310, width=310,).to_html()     
        
        context_main={
        'em_list':em_list,
        'emlistscatter':emlistscatter,    
        'fig_bar_context_b':fig_bar_context_b, 'step':step   , 'step2':step2 , 'only_for_step1':only_for_step1
        } 
        return render(request, 'chartsdetection_ml_perform.html',context_main)



def chartsdetection_detec_perfor(request):
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
        barmode = 'group'        
        )    
    fig_bar_context_b = fig_bar1.to_html()
    ##########################barchart for ML Performanve tab bar chart......ends#####
    ##################################################################################
    context_main={'fig_bar_context_b':fig_bar_context_b}
    return render(request, 'chartsdetection_detec_perfor.html',context_main)



def samplesave(request):
    if request.method == 'POST':     
        text1=request.POST.get('text')               
        remove_first_col=request.POST.get('remove_first_col')        
        id=request.POST.get('id')  
        query= text.objects.filter(id=1)
        if query:
            text.objects.filter(id=1).update(text=text1,remove_first_col=remove_first_col,id=id)
        else:
            b = text(text=text1,remove_first_col=remove_first_col,id=id)
            b.save()      

        # code to select csv from models
        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv  
                
        # code to select csv from models ends here-------

        # code to convert csv data to tabular form 
        csv_uploaded = df_table_data   # ref line no 40__This should point to the csv file you upload 
        df = ad.abstraction.data.load_dataset(csv_uploaded)        
        # code to convert csv data to tabular form ends here ------            
        
        # code for heatmap  
        steps = 2000
        scores = ad.abstraction.correlations.dtw_correlations(df, csv_uploaded, steps) 
        scores = (scores - 1) *(-1)

        column_header=list(scores.columns.values)   
        column_header2=list(scores.columns.values)     
        
        heat_fig = px.imshow(scores,x=column_header,width=500, height=500)
        heat_fig_context = heat_fig.to_html()

        # code for heatmap  ends here ------------- 

                    
        #selected dropdown code         
        temp2=text.objects.filter(id=1).values('text')
        answers_list = list(temp2)
        finaloption=answers_list[0]
        selected_value_dropdown_cur=finaloption.get("text")

        list_radio = ["no", "yes"]
        temp4=text.objects.filter(id=1).values('remove_first_col')
        answers_list_4 = list(temp4)
        finaloption_4=answers_list_4[0]
        selected_value_dropdown_colmn=finaloption_4.get("remove_first_col")         
        #selected dropdown code  ends here.... ...............................................................

        #code for bar chart  
        csv_obj_csvbar=Csv_for_heat.objects.first()
        csv_bar_file=csv_obj_csvbar.csv  
        csv_bar_file_two_readcsv = read_csv(csv_bar_file)
        data_frame_bar=pd.DataFrame(csv_bar_file_two_readcsv)

        data_frame_col_names=list(df.columns.values)
        
        obj_text_model=text.objects.first()
        dropdown_selected_bat_cur=obj_text_model.text   
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

        df_copy=None

        # if selected_value_dropdown_colmn == 'YES':
        #     #df_copy = ad.abstraction.data.remove_first_column(df)  #copy of existing df
        #     df_copy=df
        #     # run this function if remove first column is selected “YES”
        #     #generate heatmap
        #     steps = 2000
        #     dtw_scores = ad.abstraction.correlations.dtw_correlations(df_copy, csv_uploaded, steps) #generate heatmap

        #     #run test function
        #     window = 120
        #     min_iter = 6
        #     max_iter= 24
        #     start_idx = 2200 
        #     dtw_scores_conv = ad.abstraction.correlations.dtw_correlations_converge(df.iloc[:, :], files[fileSelection-1], window, min_iter=min_iter, max_iter=max_iter, start_idx = start_idx) 
        #     #files[fileSelection-1]?????
        #     #run test function
        #     #heat_fig_context=ad.abstraction.correlations.draw_correlation_graph(dtw_scores_conv, size=6)# new heat map
        #     #generate heatmap 

        #     #generate bar chart

        #     dtw_scores_conv = dtw_scores
        #     #fig_bar_context=ad.abstraction.correlations.draw_correlation_barplot(dtw_scores_conv, ground_truth_idx = ground_truth_manual)#new bar chart

        #     #generate bar chart
        #     context_main={
            
        #     "chart555": heat_fig_context,'chart66':fig_bar_context,
        #     'column_header':column_header,'column_header2':column_header2,'data_frame_col_one':data_frame_col_names,
        #     'data_frame_col_one':data_frame_col_names,       
        #     'selected_value_dropdown_cur':selected_value_dropdown_cur,
        #     'list_radio':list_radio,'selected_value_dropdown_colmn':selected_value_dropdown_colmn,       
        #     "chart555": heat_fig_context,'chart66':fig_bar_context,
        #     'column_header':column_header,'data_frame_col_one':data_frame_col_names,
        #     'data_frame_col_one':data_frame_col_names,          
        #     'dropdown_selected_bat_cur_convrt_string':dropdown_selected_bat_cur_convrt_string,       
            
        #     } 
            
        #     return render(request, 'chart1.html',context_main) 

              

          
        context_main={
            
        "chart555": heat_fig_context,'chart66':fig_bar_context,
        'column_header':column_header,'column_header2':column_header2,'data_frame_col_one':data_frame_col_names,
        'data_frame_col_one':data_frame_col_names,       
        'selected_value_dropdown_cur':selected_value_dropdown_cur,
        'list_radio':list_radio,'selected_value_dropdown_colmn':selected_value_dropdown_colmn,       
        "chart555": heat_fig_context,'chart66':fig_bar_context,
        'column_header':column_header,'data_frame_col_one':data_frame_col_names,
        'data_frame_col_one':data_frame_col_names,          
        'dropdown_selected_bat_cur_convrt_string':dropdown_selected_bat_cur_convrt_string,       
        
        } 
        
        return render(request, 'chart1.html',context_main)        

        
    else:
        return render(request,'try2.html')




def saveanamolies(request):
    if request.method == 'POST':
        all=request.POST.get('all') 
        point_anomalies=request.POST.get('point_anomalies') 
        fluctuating=request.POST.get('fluctuating') 
        bias=request.POST.get('bias') 
        dead=request.POST.get('dead') 
        cer=request.POST.get('cer') 
        cer_and_slope=request.POST.get('cer_and_slope')    
        dtw=request.POST.get('dtw') 

        id=request.POST.get('id')  
        query= inject_anamolies.objects.filter(id=1)

        if query:
            inject_anamolies.objects.filter(id=1).update(id=id,all=all,point_anomalies=point_anomalies,fluctuating=fluctuating,bias=bias,dead=dead,cer=cer,cer_and_slope=cer_and_slope,dtw=dtw)
        else:
            b = inject_anamolies(id=id,all=all,point_anomalies=point_anomalies,fluctuating=fluctuating,bias=bias,dead=dead,cer=cer,cer_and_slope=cer_and_slope,dtw=dtw)
            b.save()

    #selected checkbox code..         
    
    temp1=inject_anamolies.objects.filter(id=1).values('all')
    answers_list_1 = list(temp1)
    finaloption_1=answers_list_1[0]
    selected_checkbox_all=finaloption_1.get("all")  

    temp2=inject_anamolies.objects.filter(id=1).values('point_anomalies')
    answers_list_2 = list(temp2)
    finaloption_2=answers_list_2[0]
    selected_checkbox_point_anomalies=finaloption_2.get("point_anomalies")  

    temp3=inject_anamolies.objects.filter(id=1).values('fluctuating')
    answers_list_3 = list(temp3)
    finaloption_3=answers_list_3[0]
    selected_checkbox_fluctuating=finaloption_3.get("fluctuating")  

    temp4=inject_anamolies.objects.filter(id=1).values('bias')
    answers_list_4 = list(temp4)
    finaloption_4=answers_list_4[0]
    selected_checkbox_bias=finaloption_4.get("bias")  

    temp5=inject_anamolies.objects.filter(id=1).values('dead')
    answers_list_5 = list(temp5)
    finaloption_5=answers_list_5[0]
    selected_checkbox_dead=finaloption_5.get("dead")  

    temp6=inject_anamolies.objects.filter(id=1).values('cer')
    answers_list_6 = list(temp6)
    finaloption_6=answers_list_6[0]
    selected_checkbox_cer=finaloption_6.get("cer")  

    temp7=inject_anamolies.objects.filter(id=1).values('cer_and_slope')
    answers_list_7 = list(temp7)
    finaloption_7=answers_list_7[0]
    selected_checkbox_cer_and_slope=finaloption_7.get("cer_and_slope")  

    temp8=inject_anamolies.objects.filter(id=1).values('dtw')
    answers_list_8 = list(temp8)
    finaloption_8=answers_list_8[0]
    selected_checkbox_dtw=finaloption_8.get("dtw")             
    #selected checkbox code..  ends here .... ...............................................................
    context_main={
    'selected_checkbox_all':selected_checkbox_all,
    'selected_checkbox_point_anomalies':selected_checkbox_point_anomalies,
    'selected_checkbox_fluctuating':selected_checkbox_fluctuating,
    'selected_checkbox_bias':selected_checkbox_bias,
    'selected_checkbox_dead':selected_checkbox_dead,
    'selected_checkbox_cer':selected_checkbox_cer,
    'selected_checkbox_cer_and_slope':selected_checkbox_cer_and_slope,
    'selected_checkbox_dtw':selected_checkbox_dtw       
    } 
        
    return render(request, 'chartsdetection_inject_ano.html',context_main)


def chartsdetection_inject_ano(request):
    #selected checkbox code..         
    
    temp1=inject_anamolies.objects.filter(id=1).values('all')
    answers_list_1 = list(temp1)
    finaloption_1=answers_list_1[0]
    selected_checkbox_all=finaloption_1.get("all")  

    temp2=inject_anamolies.objects.filter(id=1).values('point_anomalies')
    answers_list_2 = list(temp2)
    finaloption_2=answers_list_2[0]
    selected_checkbox_point_anomalies=finaloption_2.get("point_anomalies")  

    temp3=inject_anamolies.objects.filter(id=1).values('fluctuating')
    answers_list_3 = list(temp3)
    finaloption_3=answers_list_3[0]
    selected_checkbox_fluctuating=finaloption_3.get("fluctuating")  

    temp4=inject_anamolies.objects.filter(id=1).values('bias')
    answers_list_4 = list(temp4)
    finaloption_4=answers_list_4[0]
    selected_checkbox_bias=finaloption_4.get("bias")  

    temp5=inject_anamolies.objects.filter(id=1).values('dead')
    answers_list_5 = list(temp5)
    finaloption_5=answers_list_5[0]
    selected_checkbox_dead=finaloption_5.get("dead")  

    temp6=inject_anamolies.objects.filter(id=1).values('cer')
    answers_list_6 = list(temp6)
    finaloption_6=answers_list_6[0]
    selected_checkbox_cer=finaloption_6.get("cer")  

    temp7=inject_anamolies.objects.filter(id=1).values('cer_and_slope')
    answers_list_7 = list(temp7)
    finaloption_7=answers_list_7[0]
    selected_checkbox_cer_and_slope=finaloption_7.get("cer_and_slope")  

    temp8=inject_anamolies.objects.filter(id=1).values('dtw')
    answers_list_8 = list(temp8)
    finaloption_8=answers_list_8[0]
    selected_checkbox_dtw=finaloption_8.get("dtw")             
    #selected checkbox code..  ends here .... ...............................................................
    context_main={
    'selected_checkbox_all':selected_checkbox_all,
    'selected_checkbox_point_anomalies':selected_checkbox_point_anomalies,
    'selected_checkbox_fluctuating':selected_checkbox_fluctuating,
    'selected_checkbox_bias':selected_checkbox_bias,
    'selected_checkbox_dead':selected_checkbox_dead,
    'selected_checkbox_cer':selected_checkbox_cer,
    'selected_checkbox_cer_and_slope':selected_checkbox_cer_and_slope,
    'selected_checkbox_dtw':selected_checkbox_dtw       
    } 
    return render(request, 'chartsdetection_inject_ano.html',context_main)




def chart2(request):
    chart2='yes'
    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv       

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
    
    temp2=text.objects.filter(id=1).values('text')
    answers_list = list(temp2)
    finaloption=answers_list[0]
    selected_value_dropdown_cur=finaloption.get("text")

    list_radio = ["no", "yes"]
    temp4=text.objects.filter(id=1).values('remove_first_col')
    answers_list_4 = list(temp4)
    finaloption_4=answers_list_4[0]
    selected_value_remove_first_col=finaloption_4.get("remove_first_col")
   
    
    context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,
    'column_header':column_header,'column_header2':column_header2,
   
    'selected_value_dropdown_cur':selected_value_dropdown_cur,'chart2':chart2,
    'list_radio':list_radio,'selected_value_remove_first_col':selected_value_remove_first_col,   
    } 
    
    return render(request, 'try2.html',context_main) 



def chart1(request):#ds_one home url function view    

    # code to select csv from models
    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv   
    
    # code to select csv from models ends here-------

    # code to convert csv data to tabular form 
    csv_uploaded = df_table_data   # ref line no 40__This should point to the csv file you upload 

    df = ad.abstraction.data.load_dataset(csv_uploaded)
    tabular_form_context=df.to_html()
    # code to convert csv data to tabular form ends here ------

    #selected dropdown code         
    temp2=text.objects.filter(id=1).values('text')
    answers_list = list(temp2)
    finaloption=answers_list[0]
    selected_value_dropdown_cur=finaloption.get("text")

    temp3=text.objects.filter(id=1).values('cut_off_thresold')
    answers_list3 = list(temp3)
    finaloption3=answers_list3[0]
    selected_value_dropdown_cut_off_thresold=finaloption3.get("cut_off_thresold")

    
    list_radio = ["no", "yes"]
    temp4=text.objects.filter(id=1).values('remove_first_col')
    answers_list_4 = list(temp4)
    finaloption_4=answers_list_4[0]
    selected_value_dropdown_colmn=finaloption_4.get("remove_first_col")         
    #selected dropdown code  ends here.... ...............................................................
    
    
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
    
    data_frame_col_names=list(df.columns.values)  
    
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

    #code for bar chart ends here-----------------
         
    context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'chart66':fig_bar_context,
    
    'column_header':column_header,'data_frame_col_one':data_frame_col_names,
    'data_frame_col_one':data_frame_col_names, 'dropdown_selected_bat_cur_convrt_string':dropdown_selected_bat_cur_convrt_string,
    'notes':notes , 'selected_value_dropdown_cur':selected_value_dropdown_cur,
    'selected_value_dropdown_colmn':selected_value_dropdown_colmn,'selected_value_cut_off_thresold':selected_value_dropdown_cut_off_thresold
    
    }     

    return render(request, 'chart1.html',context_main)




def sample2(request):    
    if request.method == 'POST':     
        text1=request.POST.get('text')
        cut_off_thresold=request.POST.get('cut_off_thresold')
                
        id=request.POST.get('id')  
        query= text.objects.filter(id=1)
        if query:
            text.objects.filter(id=1).update(text=text1,cut_off_thresold=cut_off_thresold,id=id)
        else:
            b = text(text=text1,cut_off_thresold=cut_off_thresold,id=id)
            b.save()
    
        
        # def chart() resources copied from above function-starts

        # code for selecting csv from models
        csv_obj_csvheat=Csv_for_heat.objects.first()
        df_table_data=csv_obj_csvheat.csv
        
        # code for selecting csv from models ends here --------
       
        csv_uploaded = df_table_data   # This should point to the csv file you upload 
        df = ad.abstraction.data.load_dataset(csv_uploaded)          
      
        # heat map code                  
        steps = 2000
        scores = ad.abstraction.correlations.dtw_correlations(df, csv_uploaded, steps) 
        scores = (scores - 1) *(-1) 
        column_header=list(scores.columns.values)       
        
        heat_fig = px.imshow(scores,x=column_header)
        heat_fig_context = heat_fig.to_html()
        # heat map code   ends here---------

        # code for heatmap2  
        steps2 = 2000
        scores2 = ad.abstraction.correlations.dtw_correlations(df, csv_uploaded, steps2) 
        scores2 = (scores2 - 1) *(-1)    
        
        heat_fig2 = px.imshow(scores2,x=column_header,width=800, height=800)
        heat_fig_context2 = heat_fig2.to_html()

        # code for heatmap2  ends here -------------

        # dropdown code 
        csv_obj_csvbar=Csv_for_heat.objects.first()
        csv_bar_file=csv_obj_csvbar.csv 
        csv_bar_file_two_readcsv = read_csv(csv_bar_file)

        obj_text_model=text.objects.first()# dropdown code
        text_file_selected_dropdown=obj_text_model.text        
        text_file_selected_dropdown_convrt_string=str(text_file_selected_dropdown)

        temp2=text.objects.filter(id=1).values('text')
        answers_list = list(temp2)
        finaloption=answers_list[0]
        selected_value_dropdown_cur=finaloption.get("text")

        temp3=text.objects.filter(id=1).values('cut_off_thresold')
        answers_list3 = list(temp3)
        finaloption3=answers_list3[0]
        selected_value_dropdown_cut_off_thresold=finaloption3.get("cut_off_thresold")
               
                
        # dropdown code ends

        # if selected_value_dropdown_cut_off_thresold:
        #     df = ad.abstraction.data.remove_first_column(df)  #copy of existing df
        #     # run this function if remove first column is selected “YES”
        #     #generate heatmap
        #     steps = 2000
        #     dtw_scores = ad.abstraction.correlations.dtw_correlations(df, csv_uploaded, steps) #generate heatmap

        #     #run test function
        #     window = 120
        #     min_iter = 6
        #     max_iter= 24
        #     start_idx = 2200 
        #     dtw_scores_conv = ad.abstraction.correlations.dtw_correlations_converge(df.iloc[:, :], files[fileSelection-1], window, min_iter=min_iter, max_iter=max_iter, start_idx = start_idx) 
        #     #files[fileSelection-1]?????
        #     #run test function
        #     heat_fig_context=ad.abstraction.correlations.draw_correlation_graph(dtw_scores_conv, size=6)# new heat map
        #     #generate heatmap 

        #     #generate bar chart

        #     dtw_scores_conv = dtw_scores
        #     fig_bar_context=ad.abstraction.correlations.draw_correlation_barplot(dtw_scores_conv, ground_truth_idx = ground_truth_manual)#new bar chart
        #     #generate bar chart

        #     selected_value_dropdown_cut_off_thresold_int=int(selected_value_dropdown_cut_off_thresold)
        #     parameters = ad.abstraction.input.auto_select_parameters(df, dtw_scores_conv, threshold=selected_value_dropdown_cut_off_thresold_int)
        #     df = ad.abstraction.input.select_parameters(df, ground_truth=ground_truth_manual, params=parameters) 

        #     # outfile = filename.split('.') ??
        #     # outfile = outfile[0] ??
        #     outfile='processed_csv'
        #     ad.abstraction.data.generate_featureset(df, outfile, time_column=1) 


        #     context_main={            
        #     "chart555": heat_fig_context,'chart66':fig_bar_context,
        #     'column_header':column_header,                  
        #     'selected_value_dropdown_cur':selected_value_dropdown_cur,                
        #     "chart555": heat_fig_context,'chart66':fig_bar_context,
        #     'column_header':column_header,  
        #     } 
            
        #     return render(request, 'heatmap3.html',context_main)

        

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

        #########################code for bar chart2----------------------
        fig_bar2 = px.bar(            
        data_frame = scores2[text_file_selected_dropdown_convrt_string],         
        
        # opacity = 0.9,
        orientation = "v",
        barmode = 'group',
        title='',
        )
        fig_bar2.update_yaxes(visible=False)
        fig_bar2.update_layout(showlegend=False)

        fig_bar_context2 = fig_bar2.to_html() 
        #########################code for bar chart2----------------------             

        
        return render(request,'heatmap3.html',{"chart555": heat_fig_context,'chart66':fig_bar_context,
        'column_header':column_header,'fig_bar_context2':fig_bar_context2,'heat_fig_context2':heat_fig_context2,'selected_value_dropdown_cur':selected_value_dropdown_cur,
        'selected_value_cut_off_thresold':selected_value_dropdown_cut_off_thresold,
        'label_shown':label_shown,})
    
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





def venue(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=scores.csv'
    lines=[]
    venue= Csv_score_downld.objects.all()

    for item in venue:
        lines.append(f'{item.csv}\n')
   
    response.writelines(lines)
    return response



def watchdemo(r):
    return render (r,'watchdemo.html')


def pdf2(request): 
    csv_obj_csvheat=Csv_for_heat.objects.first()
    df_table_data=csv_obj_csvheat.csv     

    # code to convert csv data to tabular form 
    csv_uploaded = df_table_data   # ref line no 40__This should point to the csv file you upload
    df = ad.abstraction.data.load_dataset(csv_uploaded)
    tabular_form_context=df.to_html(col_space='1px')
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
      
    data_frame_col_names=list(df.columns.values)  
    
    dropdown_selected_bat_cur_convrt_string = data_frame_col_names[1]      
    
    fig_bar = px.bar(            
    data_frame = scores[dropdown_selected_bat_cur_convrt_string],         
    
    # opacity = 0.9,
    orientation = "v",
    barmode = 'group',
    title='',
    width=800,
    )
    fig_bar.update_yaxes(visible=False)
    fig_bar.update_layout(showlegend=False)

    fig_bar_context = fig_bar.to_html()    

    #code for bar chart ends here-----------------
    context_main={'dfr': tabular_form_context, "chart555": heat_fig_context,'chart66':fig_bar_context,
    'column_header':column_header,'data_frame_col_one':data_frame_col_names,
    'data_frame_col_one':data_frame_col_names,  'dropdown_selected_bat_cur_convrt_string':dropdown_selected_bat_cur_convrt_string,
    
    
    }   
    return render(request, 'pdf2.html',context_main)






def try2(request):#ds_one home url function view     
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



    
    





    







    


  








