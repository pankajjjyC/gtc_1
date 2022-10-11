# -*- coding: utf-8 -*-
# import standard packages
import dash
from dash import dcc
from dash import html
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import numpy as np 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from obspy.clients.neic import Client
from obspy import UTCDateTime
import time

from django_plotly_dash import DjangoDash

import seisbench.models as sbm
import matplotlib.pyplot as plt







#app = dash.Dash(__name__)
google_roboto = 'https://fonts.googleapis.com/css2?family=Roboto&display=swap'
external_stylesheets = [google_roboto, dbc.themes.BOOTSTRAP]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from ds_two import preprocess as rdl


app = DjangoDash('dash_app_new',external_stylesheets=external_stylesheets, title='Seismic AI') # django app




####################
## Tab style info ##
####################

# These are some colors
color_dash_blue = "#119DFF"
color_lime_green = "#32C52C"
color_green = "#65DC61"
color_blue = "#61A3DC"

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': color_blue,
    'color': 'white',
    'padding': '6px'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}


#########################
## Create the dash app ##
#########################

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Seismic AI')
#import preprocess as rdl





###############
## Functions ##
###############

def get_data(net, station, loc, chan, time_start, time_stop):
    client = Client()
    stream = client.get_waveforms(net, station, loc, chan, time_start, time_stop)
    channels = []
    waveforms = []
    times = []
    for trace in stream:
        channel = trace.stats['channel']
        channels.append(channel)
        
        waveform = trace.data
        waveforms.append(waveform)
        
        time = trace.times("utcdatetime")
        times.append(time)

        sampling_rate = trace.stats['sampling_rate']
        sampling_rate = float(sampling_rate)
        
    return channels, waveforms, times, sampling_rate , stream



def plot_waveforms(channels, waveforms, times, plot_title):
    fig = go.Figure()
    
    for idx, waveform in enumerate(waveforms):
        x = times[idx]
        channel = channels[idx]
        fig.add_trace(go.Scatter(x=x, y=waveform, name=channel))
    
    fig.update_layout(legend_title_text='Channel', 
                    showlegend=True, title=plot_title,
                    xaxis_title="Date/time", yaxis_title='signal',
                    margin=dict(l=10, r=10, t=40, b=1))
    
    return fig


def plot_waveforms_processed(channels, waveforms, times, plot_title):
    n_channels = len(channels)
    fig = make_subplots(rows=n_channels, cols=1, shared_xaxes=True)
    
    for idx, waveform in enumerate(waveforms):
        x = times[idx]
        channel = channels[idx]
        fig.add_trace(go.Scatter(x=x, y=waveform, name=channel),row=idx+1, col=1)
        #fig.update_xaxes(title_text="xaxis {} title".format(idx), row=idx+1, col=1)
        #fig.update_yaxes(title_text="yaxis {} title".format(idx), row=idx+1, col=1)
        
    fig.update_layout(legend_title_text='Channel', 
                    showlegend=True, title=plot_title,
                    xaxis_title="Date/time", yaxis_title='signal',
                    margin=dict(l=10, r=10, t=40, b=1))
    
    return fig


def create_map(lat=33.411, lon=-83.467):


    fig = go.Figure(data=go.Scattergeo(lat=[lat], lon=[lon],
                                   text= ['GOGA'],
                                   locationmode = 'USA-states',))
    fig.update_layout(
        geo = dict(
            scope='usa',
            projection_type='albers usa',
            #showland = True,
            #landcolor = "rgb(250, 250, 250)",
            #subunitcolor = "rgb(217, 217, 217)",
            #countrycolor = "rgb(217, 217, 217)",
            #countrywidth = 0.5,
            #subunitwidth = 0.5
            ),
        )
    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)
    fig.update_layout(margin=dict(l=2, r=2, t=2, b=2))

    return fig


fig_map = create_map()


###############
## Title bar ##
###############
logo = html.Img(className='logo', src='/assets/Logo_for_dark_background_green.png', height='100px')

title_text_div = html.Div(className="title_text",
    children=[
        #html.H1("Main Title", className="title"),
        #html.H3("Subtitle")
        ]
    )


title_div = html.Div(className="title_block",
    children=[
        #logo,
        #title_text_div
        ]
    )


###########
## Tab 1 ##
###########

tab1_subtitle = html.H3("Tab 1")

# Put tab 1 stuff here
title_waveform_selection = html.H3('Waveform parameters')

div_time_date_selection = html.Div([
    #html.Div(['Date/time ending (default: now)',dcc.Input(id='datetime_end', type='text')]),
    html.Div(['Window length (seconds)', dcc.Input(id='duration',
                                                type='number', 
                                                value=300,
                                                min=1, 
                                                max=60*60)])
    ],style={'visibility':'hidden'})



div_signal_raw = html.Div(className="no_class",
    children=[
    dcc.Graph(id='fig_signal_raw',
            config={'displayModeBar':False},
            style={'width':800, 
                'height':250})
    ])

div_fig_map = html.Div(className="map_div",
    children=[
    dcc.Graph(id='fig_map',
            figure=fig_map,
            config={'displayModeBar':False},)
    ])

# Put tab 1 stuff here

tab1_content = html.Div(className="tab_content",
    children=[
    #tab1_subtitle,
    # Pack all of tab 1 stuff,
    title_waveform_selection ,
    div_time_date_selection,
    div_signal_raw,
    div_fig_map

    ])

tab1 = dcc.Tab(label="Tab 1 name",children=tab1_content,
    style=tab_style, selected_style=tab_selected_style)


###########
## Tab 2 ##
###########

tab2_subtitle = html.H3("Tab 2")

# Put tab 2 stuff here
title_waveform_analysis = html.H3('Waveform analysis')

div_signal_processing = html.Div([
    html.Div(['Detrend: ', dcc.RadioItems(['no', 'yes'], 'no', id='detrend', inline=True)]),
    html.Div(['Bandpass: ', dcc.RadioItems(['no', 'yes'], 'no', id='bandpass', inline=True)]),
    html.Div([dcc.RangeSlider(.5, 10, .5, value=[.5, 10], id='bandpass_range')], style={'width':500})

    ])

button_process_data = html.Button('Process waveforms', id='button_process_waves', 
        className="button", n_clicks=0)

div_signal_processed = html.Div(className="no_class",
    children=[
    dcc.Graph(id='fig_signal_processed',
            config={'displayModeBar':False},
            style={'width':800, 
                'height':450})
    ])
# Put tab 2 stuff here

tab2_content = html.Div(className="tab_content",
    children=[
    #tab2_subtitle,
    # Pack all of tab 2 stuff,
    title_waveform_analysis,
    div_signal_processing,
    button_process_data,
    div_signal_processed
    ])

tab2 = dcc.Tab(label="Tab 2 name",children=tab2_content,
    style=tab_style, selected_style=tab_selected_style)



###########
## Tab 3 ##
###########

tab3_subtitle = html.H3("Denoiser Waveform")

button_process_data = html.Button('Apply Deep Denoiser Output', id='denoiser_output', 
        className="button", n_clicks=0)

div_waveform_processed = html.Div(className="no_class",
    children=[
    dcc.Graph(id='fig_waveform_processed',
            config={'displayModeBar':False},
            style={'width':800, 
                'height':450})
    ])

# Put tab 3 stuff here

tab3_content = html.Div(className="tab_content",
    children=[
    tab3_subtitle,
    # Pack all of tab 3 stuff,
    button_process_data,
    div_waveform_processed


    ])

tab3 = dcc.Tab(label="Tab 3 name",children=tab3_content,
    style=tab_style, selected_style=tab_selected_style)


################
## Tab layout ##
################
tab_layout = dcc.Tabs([
                    tab1,
                    tab2,
                    tab3],
    vertical=True)



###############
## Callbacks ##
###############
@app.callback(
    Output(component_id='fig_signal_raw', component_property='figure'),
    Output('store_waveforms_raw','data'),
    Output('store_waveforms_times','data'),
    Output('store_sampling_rate','data'),
    Output('store_channels','data'),
    Output('store_data_loaded','data'),
    Input('url', 'pathname'),
    Input('duration', 'value'),
    State('store_station','data'),
    State('store_net','data'),
    State('store_chan','data'),
    State('store_loc','data'),
    State('store_data_loaded','data'),
    prevent_initial_call=False)
def callback_get_raw_data_plot(url, window_length, station, net, chan, loc, data_loaded):

    now=UTCDateTime()
    time_start = now-window_length
    time_stop = now

    #print("Getting data")
    channels, waveforms, times, sampling_rate = get_data(net, station, loc, chan, time_start, time_stop)

    #print('Creating plot')
    plot_title = 'Station: {}'.format(station)
    fig_raw_signal = plot_waveforms(channels, waveforms, times, plot_title)

    data_loaded = data_loaded + 1

    return fig_raw_signal, waveforms, times, sampling_rate, channels, data_loaded



##############
@app.callback(
    Output(component_id='fig_signal_processed', component_property='figure'),
    Output('store_waveforms_processed','data'),
    Input('store_data_loaded', 'data'),#data_loaded
    Input('detrend', 'value'),#detrend
    Input('bandpass', 'value'),#bandpass
    Input('bandpass_range', 'value'),#bandpass_range
    State('store_waveforms_raw','data'),#waveforms
    State('store_waveforms_times','data'),#times
    State('store_sampling_rate','data'),#sampling_rate
    State('store_station','data'),#station
    State('store_channels','data'),#channels
    
    prevent_initial_call=True)
def callback_process_waves(data_loaded, detrend, bandpass, bandpass_range, waveforms, times, sampling_rate, station, channels):
    lowpass_cutoff, highpass_cutoff = bandpass_range


    waveforms_processed = []

    for waveform in waveforms:

        if detrend == 'yes':
            waveform = rdl.detrend(waveform)

        if bandpass == 'yes':
            waveform == rdl.taper(waveform, taper_fraction=0.05)
            waveform = rdl.bandpass_filter(waveform, lowpass_cutoff, highpass_cutoff, sampling_rate, order=4)

        waveforms_processed.append(waveform)

    plot_title = 'Station: {}, processed signal'.format(station)
    fig_process_signal = plot_waveforms_processed(channels, waveforms_processed, times, plot_title)

    return fig_process_signal, waveforms_processed

##############
@app.callback(
    Output(component_id='fig_waveform_processed', component_property='figure'),
    Output('store_waveforms_denoiser','data'),
    Input('url', 'pathname'),
    Input('duration', 'value'),
    State('store_station','data'),
    State('store_net','data'),
    State('store_chan','data'),
    State('store_loc','data'),
    State('store_data_loaded','data'),
    

    
    prevent_initial_call=True)
def callback_denoiser_waves(url, window_length, station, net, chan, loc, data_loaded):
    now=UTCDateTime()
    time_start = now-window_length
    time_stop = now

    channels, times, stream = get_data(net, station, loc, chan, time_start, time_stop)

    model = sbm.DeepDenoiser.from_pretrained("original")
    
    annotations = model.annotate(stream)   
    trace1=annotations[0]
    x=trace1.data

    trace2=annotations[1]
    y=trace2.data

    trace3=annotations[2]
    z=trace1.data




    waveforms_processed = np.array([x,y,z])

    plot_title = 'Station: {}, processed signal'.format(station)
    fig_process_signal = plot_waveforms_processed(channels, waveforms_processed, times, plot_title)

    return fig_process_signal, waveforms_processed

################
## App layout ##
################

app.layout = html.Div(className='main_div',
    children=[
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='store_data_loaded', data=0), # used to activate the processing callback once the data is loaded
        dcc.Store(id='store_waveforms_raw', data=None),
        dcc.Store(id='store_waveforms_times', data=None),
        dcc.Store(id='store_sampling_rate', data=None),
        dcc.Store(id='store_waveforms_processed', data=None),
        dcc.Store(id='store_waveforms_denoiser', data=None),
        dcc.Store(id='store_channels', data=None),
        dcc.Store(id='store_net', data='US'),
        dcc.Store(id='store_station', data='GOGA'),
        dcc.Store(id='store_chan', data='BH?'),
        dcc.Store(id='store_loc', data='00'),
        dcc.Interval(id="interval_1_sec", n_intervals=1, max_intervals=-1, interval=1000), #1000 milliseconds
        ###
        title_div,
        tab_layout
    ])


# if __name__ == "__main__":
#     app.run_server(debug=True)
#     #app.run_server(debug=False, port=80, host="0.0.0.0")