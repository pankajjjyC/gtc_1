import seisbench.models as sbm
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import matplotlib.pyplot as plt
from dash import html#dash means plotly dash
from dash import dcc 
from django_plotly_dash import DjangoDash
import pandas as pd
import plotly.express as px 
import dash
import dash_bootstrap_components as dbc

google_roboto = 'https://fonts.googleapis.com/css2?family=Roboto&display=swap'
external_stylesheets = [google_roboto, dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Seismic AI')

import preprocess as rdl

client = Client("GFZ")

t = UTCDateTime("2014/04/02 05:47:50")
stream = client.get_waveforms(network="CX", station="PB01", location="*", channel="HH?", starttime=t, endtime=t+200)
fig1=stream.plot()

model = sbm.DeepDenoiser.from_pretrained("original")
annotations = model.annotate(stream)
fig2=annotations.plot()


app.layout=html.Div([

    html.H1('Hello 3d Data',style={'color':'red','paddingLeft':'200px','fontSize':'100px'}),
    dcc.Graph(figure=fig1,style={'position':'relative','left':'200px'}),
    dcc.Graph(figure=fig2,style={'position':'relative','top':'200px'}),

])



if __name__ == "__main__":
    app.run_server(debug=True)