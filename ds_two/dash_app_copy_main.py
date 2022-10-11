# -*- coding: utf-8 -*-


# import standard packages
import numpy as np 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from obspy.clients.neic import Client
from obspy import UTCDateTime
import time

import dash 
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash

app = dash.Dash(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#import dash_daq as daq
#from dash_styles import *

# using 
# path_to_package = '/mnt/c/Users/jwilliams/Documents/GitHub/7139_USAF_Seismic_ML'
# import sys
# sys.path.append(path_to_package)
# from ds_two import preprocess as rdl
import preprocess as rdl

print('Reloading Program')

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
        
    return channels, waveforms, times, sampling_rate



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



###################
## make dash app ##
###################

# Set up login system
#import dash_auth
#VALID_USERNAME_PASSWORD_PAIRS = {'GTC':'Gtc1160!', 'DOE':'smartfrac'}

# Create the dash app
google_roboto = 'https://fonts.googleapis.com/css2?family=Roboto&display=swap'
external_stylesheets = [google_roboto, dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Seismic AI')
# app = DjangoDash('dash_app_copy_main',external_stylesheets=external_stylesheets) # django app
#auth = dash_auth.BasicAuth(app,VALID_USERNAME_PASSWORD_PAIRS)





###############
## Title bar ##
###############
logo = html.Img(className='logo', src='/assets/Logo_for_dark_background_green.png', height='75px')

title_text_div = html.Div(className="title_text",
    children=[
        html.H2("Seismic AI", className="title"),
        html.H3("Global Technology Connection, Inc.")
        ]
    )

title_div = html.Div(className="title_block",
    children=[
        logo,
        title_text_div
        ]
    )



##############
## Main Div ##
##############

title_waveform_selection = html.H3('Waveform parameters')

div_time_date_selection = html.Div([
    #html.Div(['Date/time ending (default: now)',dcc.Input(id='datetime_end', type='text')]),
    html.Div(['Window length (seconds)', dcc.Input(id='duration',
                                                type='number', 
                                                value=300,
                                                min=1, 
                                                max=60*60)])
    ])

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


main_div = html.Div(className="main_div",
    children=[
        title_waveform_selection,
        div_time_date_selection,
        div_signal_raw,
        div_fig_map,
        title_waveform_analysis,
        div_signal_processing,
        #button_process_data,
        div_signal_processed
        ])



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
    
    Input('detrend', 'value'),
    Input('bandpass', 'value'),
    Input('bandpass_range', 'value'),

    Input('store_data_loaded', 'data'),
    State('store_waveforms_raw','data'),
    State('store_waveforms_times','data'),
    State('store_sampling_rate','data'),
    State('store_station','data'),
    State('store_channels','data'),
    
    prevent_initial_call=True)
def callback_process_waves(data_loaded, waveforms, times, sampling_rate, station, channels, detrend, bandpass, bandpass_range):
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
        dcc.Store(id='store_channels', data=None),
        dcc.Store(id='store_net', data='US'),
        dcc.Store(id='store_station', data='GOGA'),
        dcc.Store(id='store_chan', data='BH?'),
        dcc.Store(id='store_loc', data='00'),
        dcc.Interval(id="interval_1_sec", n_intervals=1, max_intervals=-1, interval=1000), #1000 milliseconds
        #dcc.Interval(id="interval_5_sec", n_intervals=1, max_intervals=-1, interval=5000), #5000 milliseconds
        # title_div,
        main_div
    ])


if __name__ == "__main__":
    app.run_server(debug=True, port=8143)
    #app.run_server(debug=False, port=8143, host="0.0.0.0")