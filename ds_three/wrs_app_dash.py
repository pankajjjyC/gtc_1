import pandas as pd
import numpy as np
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64

import dash  # (version 1.12.0) pip install dash
from dash import dcc
import dash_daq as daq
from dash import html
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash

app = dash.Dash(__name__)

from Paragon_WRS import *
import numpy as np
#test.ping()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = DjangoDash('dash_app_wrs',external_stylesheets=external_stylesheets) # django app

d_ctrls_i = ["const", 'False', 'False', 'Lin', 'Lin']
x_l,y_l,k_l,Q_l,KH_l,KC_l,FR_l,u_l, d_x, d_y,d_k,d_Q,d_KH,d_KC,d_FR,d_u = Run_m.run_wrs_m(5, d_ctrls_i)
fig1 = px.line(d_k, y = ['k_in','k_p4', 'k_p5','k_p8'], title = "Water Conductivity")
fig1.data[0].name = "Inlet Water"
fig1.data[1].name = "Post Carbon Cartridge"
fig1.data[2].name = "Post IX Cartridge"
fig1.data[3].name = "Product Water"
fig1.update_layout(legend_x=0.05, legend_y=0.6)

fig3 = px.line(d_FR, y = 'FR_f1', title = "Filter Health")

# fig3 = px.line(x= Q_l[:,2] - Q_l[-1,2], y = FR_l[:,1])

fig4_1 = px.line(d_y, y = ['q_f1'])
fig4_2 = px.line(d_x, y = ['p_f1'])
fig4_2.update_traces(yaxis="y2")
# Create figure with secondary y-axis
fig4 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig4.add_traces(fig4_1.data + fig4_2.data)
fig4.data[0].name = "Flow Rate"
fig4.data[1].name = "Pressure Differential"
fig4.layout.xaxis.title="Time"
fig4.layout.yaxis.title="Flow Rate [LPH]"
fig4.layout.yaxis2.title="Pressure"
fig4.update_layout(legend_x=0.6, legend_y=0.05)
fig4.layout.title="Key Filter Parameters"
fig4.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))


fig5 = px.bar(d_KH.iloc[-1])
fig5.layout.yaxis.title = "Remaining Useful Life [Liters]"
fig5.layout.showlegend=False
fig6 = px.line(d_KC, y = ['KC_MABR','KC_f1', 'KC_f2', 'KC_f3', 'KC_f4', 'KC_s1', 'KC_f5'])

test_png = 'gtc_logo.png'


app.layout = html.Div([
    html.Div([
        # html.H1("GTC",style={'color': 'white','width':"10%", 'height':"60px", 'display': 'inline-block'}),
        # html.H1("Bio-Physiochemical WRS Demo",style={'width':'79%', 'color': 'white', 'display': 'inline-block', 
        # 'text-align':'center','height':"60px",  "font-weight": "bold"}), 
        # html.H1("Paragon", style={'color': 'white','width':"10%", 'height':"60px", 'display': 'inline-block'})
        ], style = {'width':'100%', 'height':"0px", 'display': 'inline-block','background-color':"white"}),#60px changed to 0px

    # html.Div(html.H1("Paragon Bio-Physiochemical WRS Demo"),style={'color': 'white', 
    # 'text-align':'center', "font-weight": "bold", 'background-color':"#231F4A"}),

    html.Div([
    html.Div([
        html.Br(),
        html.Div("INSTRUCTIONS TO RUN DEMO:", style={"font-weight": "bold", 'text-align':'left','background-color':"white"}),
        html.Br(),
        html.Div("1. Change assumptions as necessary"),
        html.Br(),
        html.Div("2. Input number of hours of test run, and"),
        html.Br(),
        html.Div("3. Click on 'Run Demo' button"),
        html.Br(),
        html.Div("4. Click on Filter/Cartridge replace button during run"),
        html.Br(),
        html.Div("Input length of run in hours"),
        # html.Br(),
        html.Div(["Run Time (Hr): ",
                dcc.Input(id='sim_hrs', value=5, type='number')]),
        html.Br(),
        html.Button('Run Demo', id='Run_sim_btn', n_clicks=0, style={'background-color':"white"}) 
        ],style={'width': '50%', 'display': 'inline-block', 'background-color':"white"}),
    
    html.Div([
        html.Div("ASSUMPTIONS:", style={"font-weight": "bold", 'text-align':'left','background-color':"white"}),
        
        html.Div(["Inlet Water Conductivity:"],
            style = {'width': '35%', 'display': 'inline-block','background-color':"white"}), 
        
        html.Div([dcc.Dropdown(
            id='cond_in', options=[
            {'label': 'Constant', 'value': 'const'},
            {'label': 'Random Walk', 'value': 'rand_walk'}],
            value='const')],style={'width': '30%', 'display': 'inline-block','background-color':"white"}),
        html.Br(),
        html.Br(),
        html.Div([daq.ToggleSwitch(
        id='f_clog', label='Filter Clogging' , color="#231F4A", labelPosition='top', value=False)],
        style={'width': '30%', 'display': 'inline-block', 'background-color':"white"}),
        
        html.Div([daq.ToggleSwitch(
        id='c_degr', label='Cartridge Degradation', 
        labelPosition='top', value=False, color="#231F4A")], style={'width': '30%', 'display': 'inline-block','background-color':"white"}),
       
        html.Div([html.Br()]),
        

        html.Div(["Filter Clogging Mode:"], 
        style={'width': '35%', 'display': 'inline-block' , 'background-color':"white"}),
        
        html.Div([dcc.Dropdown(
            id='f_deg_mode', options=[
            {'label': 'Linear', 'value': 'Lin'},
            {'label': 'Advanced', 'value': 'Adv'}],
            value='Lin')] ,style={'width': '30%', 'display': 'inline-block', 'background-color':"white"}),

        html.Div([html.Br()]),
        
        html.Div(["Cartridges Degradation Mode:"], 
        style={'width': '35%', 'display': 'inline-block' , 'background-color':"white"}), 
        
        html.Div([dcc.Dropdown(
            id='c_deg_mode', options=[
            {'label': 'Linear', 'value': 'Lin'},
            {'label': 'Advanced', 'value': 'Adv'}],
            value='Lin')],style={'width': '30%', 'display': 'inline-block', 'background-color':"white"}),

        html.Div([html.Br()]),
  
#         html.Div(
#             [html.Button('Filter Replacement', id='f_r_btn', n_clicks=0, style={'background-color':"white"}) 
#         ], style={'width': '35%', 'display': 'inline-block'}),
#         html.Div(
#             [html.Button('Cartridge Replacement', id='c_r_btn', n_clicks=0, style={'background-color':"white"}) 
#         ], style={'width': '35%', 'display': 'inline-block'}),

    ],style={'width': '50%', 'display': 'inline-block',  "background-color":"white"}),
    
    html.Div([
        html.Br(), 
        html.Br() ]),

   html.Div([
        html.Div("FILTER HEALTH:", style={"font-weight": "bold", 'text-align':'left'}),
        html.Br(),
        html.Div(["WRS Model Estimated:"], style={"font-weight": "bold","width": "100%", 'text-align':'left','background-color':"white"}),
        # html.Div(["RUL (%):"], style={"width": "20%", 'text-align':'center'}),
        
        html.Div(style={"width": "10%", "background-color":"", "height":"60px", 'display': 'inline-block','background-color':"white"}), 
        html.Div([
        html.P(id ='mod_est_rul_perc'),
        # html.Div(["RUL (Liters):"], style={"width": "20%", 'text-align':'center'}),
        html.Div(id ='mod_est_rul_lit')], style={"width": "30%", 'display': 'inline-block'}),
        html.Br(),
        html.Div(["Manufacturer Recommended:"], style={"font-weight": "bold","width": "100%", 'text-align':'left','background-color':"white"}),
        # html.Div(["RUL (%):"], style={"width": "45%", 'text-align':'left'}),
        html.Div(style={"width": "10%", "background-color":"", "height":"60px", 'display': 'inline-block'}), 
        html.Div([
        html.P(id ='mfg_rec_rul_perc'),
        # html.Div(["RUL (Liters):"], style={"width": "20%", 'text-align':'center'}),
        html.Div(id ='mfg_rec_rul_lit')], style={"width": "30%", 'text-align':'left', 'display': 'inline-block','background-color':"white"}),
        html.Br(),
        ],style={'width': '50%', 'display': 'inline-block', "background-color":"white"}),

    
    html.Div([
        html.Div("WRS PARAMETERS:", style={"font-weight": "bold", 'text-align':'left','background-color':"white"}),
        html.Br(),
        html.Div([
        html.P(id ='pump_status'),
        # html.Div(["RUL (Liters):"], style={"width": "20%", 'text-align':'center'}),
        html.P(id ='prod_rate'),
        # html.Div(["RUL (%):"], style={"width": "45%", 'text-align':'left'}),
        html.P(id ='inlet_cond'),
        # html.Div(["RUL (Liters):"], style={"width": "20%", 'text-align':'center'}),
        html.P(id ='postix_cond'),
        html.Div(id ='prod_cond')], style={"width": "50%", 'text-align':'left', 'display': 'inline-block','background-color':"white"}),
        html.Br(),
        html.Br()
        ],style={'width': '50%', 'display': 'inline-block',  "background-color":"white", 'justify':'top','background-color':"white"}),


    
        html.Br(), 
        html.Br() ], style={ "background-color":"white"}),


    html.Div([
    
    html.Div([

        html.Div(dcc.Graph(id='graph1', figure=fig1), style={"border":"2px black solid", 'background-color':"white"})
        ],style={'width': '49%', 'padding':'0.5%', 'display': 'inline-block', 'height':'450px'}),# yahan se karna hai color
    

    html.Div([
        html.Div([
        html.Br(),
        html.Div("Tank Levels", style ={"font-weight": "bold", 'text-align':'center'}),
        # html.Div("MABR & Accumulator Tank Levels:", style={"font-weight": "bold", 'text-align':'center'}),
        html.Br(),
        html.Div([
        daq.Tank(
        id='mabr_tank',
        height=300,
        width=150,  
        value=100,
        min=0,
        max=100,
        showCurrentValue = True,
        units = "PERCENT"), html.Div("MABR Tank", style={'text-align':'center'})],
        style={'margin-left': '60px', 'width': '25%', 'display': 'inline-block', 'background-color':'white'}),

        html.Div([

        ],style={'width': '25%', 'display': 'inline-block'}),


        html.Div([
        daq.Tank(
        id='acc_tank',
        height=300,
        width=150,  
        value=0,
        min=0,
        max=100,
        showCurrentValue = True,
        units = "PERCENT"), html.Div("Acc. Tank", style={'text-align':'center'})],
        style={'margin-left': '60px', 'width': '25%', 'display': 'inline-block', 'background-color':'white'}),
        ], style={"border":"2px black solid",'height':'450px', 'background-color':'white'})
        ],style={'width': '49%','padding':'0.5%',
         'display': 'inline-block', 'height':'450px', 'vertical-align': 'top'}),

    html.Div([

        html.Div(dcc.Graph(id='graph3', figure=fig3), style={"border":"2px black solid"})
        ],style={'width': '49%','padding':'0.5%', 'display': 'inline-block', 'height':'450px'}),


    html.Div([

        html.Div(dcc.Graph(id='graph4', figure=fig4), style={"border":"2px black solid"})
        ],style={'width': '49%','padding':'0.5%', 'display': 'inline-block', 'height':'450px'}),

    html.Div([

        html.Div(dcc.Graph(id='graph5', figure=fig5), style={"border":"2px black solid"})
        ],style={'width': '49%','padding':'0.5%', 'display': 'inline-block', 'height':'450px'}),


    html.Div([

        html.Div(dcc.Graph(id='graph6', figure=fig6), style={"border":"2px black solid"})
        ],style={'width': '49%','padding':'0.5%', 'display': 'inline-block', 'height':'450px'}),

    ],style={'background-color':'#231F4A'} )

])



# @app.callback(
#     Output(component_id='mod_est_rul_perc', component_property='children'),
#     Output(component_id='mod_est_rul_lit', component_property='children'),
#     Output(component_id='mfg_rec_rul_perc', component_property='children'),
#     Output(component_id='mfg_rec_rul_lit', component_property='children'),
#     Input('Run_sim_btn', 'n_clicks'),
#     State(component_id='sim_hrs', component_property='value'))
# def update_output_div(n_clicks, input_value):
#     rul_1 = input_value*1
#     rul_2 = input_value*2
#     rul_3 = input_value*3
#     rul_4 = input_value*4
#     # return 'RUL (%): {}'.format(rul_1),'RUL (Liters): {}'.format(rul_2),'RUL (%): {}'.format(rul_3),'RUL (Liters): {}'.format(rul_4),

#     return 'RUL (%): TBD','RUL (Liters): TBD', 'RUL (%): TBD','RUL (Liters): TBD'


# @app.callback(
#     Output(component_id='pump_status', component_property='children'),
#     Output(component_id='prod_rate', component_property='children'),
#     Input('Run_sim_btn', 'n_clicks'),
#     State(component_id='sim_hrs', component_property='value'))
# def update_output_div(n_clicks, input_value):
#     rul_1 = "ON"
#     rul_2 = 100
#     return 'WRS Pump Status: {}'.format(rul_1), 'Production Rate (LPH): {}'.format(rul_2)

# @app.callback(
#     Output(component_id='inlet_cond', component_property='children'),
#     Output(component_id='postix_cond', component_property='children'),
#     Output(component_id='prod_cond', component_property='children'),
#     Input('Run_sim_btn', 'n_clicks'),
#     State(component_id='sim_hrs', component_property='value'))
# def update_output_div(n_clicks, input_value):
#     rul_3 = 250
#     rul_4 = 20
#     rul_5 = 5
#     return 'Inlet Water Conductivity (uS/cm): {}'.format(rul_3),'Post IX Conductivity (uS/cm): {}'.format(rul_4), 'Product Water Conductivity: (uS/cm): {}'.format(rul_5)



@app.callback(
    Output(component_id="graph1", component_property='figure'),
    Output(component_id="graph3", component_property='figure'),
    Output(component_id="graph4", component_property='figure'),
    Output(component_id="graph5", component_property='figure'),
    Output(component_id="graph6", component_property='figure'),
    dash.dependencies.Output('mabr_tank', 'value'),
    dash.dependencies.Output('acc_tank', 'value'),
    Output(component_id='mod_est_rul_perc', component_property='children'),
    Output(component_id='mod_est_rul_lit', component_property='children'),
    Output(component_id='mfg_rec_rul_perc', component_property='children'),
    Output(component_id='mfg_rec_rul_lit', component_property='children'),
    Output(component_id='pump_status', component_property='children'),
    Output(component_id='prod_rate', component_property='children'),
    Output(component_id='inlet_cond', component_property='children'),
    Output(component_id='postix_cond', component_property='children'),
    Output(component_id='prod_cond', component_property='children'),

    # Output(component_id='pump_status', component_property='children'),
    # Output(component_id='prod_rate', component_property='children'),
    # Output(component_id='inlet_cond', component_property='children'),
    # Output(component_id='postix_cond', component_property='children'),
    # Output(component_id='prod_cond', component_property='children'),

    Input('Run_sim_btn', 'n_clicks'),
    State(component_id='cond_in', component_property='value'),
    State(component_id='f_clog', component_property='value'),
    State(component_id='c_degr', component_property='value'),
    State(component_id='f_deg_mode', component_property='value'),
    State(component_id='c_deg_mode', component_property='value'),
    State(component_id='sim_hrs', component_property='value')
    )
def update_plot(n_clicks, cond_in, f_clog, c_degr,f_d_mode,c_d_mode, sim_hrs):
    d_ctrls = [cond_in, f_clog, c_degr, f_d_mode, c_d_mode]
    x_l,y_l,k_l,Q_l,KH_l,KC_l,FR_l,u_l, d_x, d_y,d_k,d_Q,d_KH,d_KC,d_FR,d_u = Run_m.run_wrs_m(sim_hrs, d_ctrls)
    

    
    fig1 = px.line(d_k, y = ['k_in','k_p4', 'k_p5', 'k_p8'], title = "Water Conductivity")
    fig1.data[0].name = "Inlet Water"
    fig1.data[1].name = "Post Carbon Cartridge"
    fig1.data[2].name = "Post IX Cartridge"
    fig1.data[3].name = "Product Water"
    fig1.layout.xaxis.title="Time [min]"    
    fig1.layout.yaxis.title="Conductivity (uS/cm)"
    fig1.update_layout(legend_x=0.02, legend_y=0.98) 
    
    
    Q_Fil, Fil_HP, FHP_thr, Time, Liters = RUL_m.RUL_Fil(x_l,y_l,k_l,Q_l,KH_l,KC_l,FR_l,u_l,d_ctrls, 24)
    
    if Time == None:
        rul_1 = str(round((Fil_HP[0] - FHP_thr[0])*100/(FR_l[0,1]- FHP_thr[0]),1))
        
        mul_fac = ((Fil_HP[0] - FHP_thr[0])*100/(FR_l[0,1]- FHP_thr[0]) - (Fil_HP[-1] - FHP_thr[0])*100/(FR_l[0,1]- FHP_thr[0]))
        liters = 100*Q_Fil[-1]*1000/mul_fac
        
        rul_2 = str(round(liters,0))
    
#     fig3_1 = px.line(x= Q_l[:,2] - Q_l[-1,2], y = FR_l[:,1])
#     fig3_2 = px.line(x = Q_Fil, y=Fil_HP)
#     fig3_3 = px.line(x = Q_Fil, y = FHP_thr)
# #     fig3 = fig3_2
#     fig3.add_traces(fig3_1.data + fig3_2.data + fig3_3.data)
    
    fig3 = px.line(d_FR, y = ['FR_f1'], title = "Filter Health", labels = {"time(min)": "Time [min]", "value":"Flow Conductance"})
    fig3.layout.showlegend = False
    
    fig4_1 = px.line(d_y*1000*3600, y = ['q_f1'])
    fig4_2 = px.line(d_x, y = ['p_f1'])
    fig4_2.update_traces(yaxis="y2")
    # Create figure with secondary y-axis
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig4.add_traces(fig4_1.data + fig4_2.data)
    fig4.data[0].name = "Flow Rate"
    fig4.data[1].name = "Pressure Diff."
    fig4.layout.xaxis.title="Time [min]"
    fig4.layout.yaxis.title="Flow Rate [LPH]"
    fig4.layout.yaxis2.title="Pressure [Pascal]"
    fig4.layout.title="Key Filter Parameters"
    fig4.update_layout(legend_x=0.7, legend_y=0.02)
    fig4.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

    fig5 = px.bar(d_KH.iloc[-1])

    fig5.update_layout(
    # font_family="Courier New",
    # font_color="blue",
    title="Manufacturers' Recommended RUL",
    # title_font_family="Times New Roman",
    # title_font_color="red",
    yaxis_title="Remaining Useful Life [Liters]",
    xaxis_title="Component",
    showlegend=False
    # legend_title_font_color="green"
    )


    fig6 = px.line(d_KC, y = ['KC_MABR','KC_f1', 'KC_f2', 'KC_f3', 'KC_f4', 'KC_s1', 'KC_f5'], title= "Conductivity Transmitance")
    fig6.layout.xaxis.title = "Time [min]"
    fig6.layout.yaxis.title = "Conductivity Transmitance"
    fig6.data[0].name = "MABR" 
    fig6.data[1].name = "Micron-Filter" 
    fig6.data[2].name = "Carbon Cart."
    fig6.data[3].name = "IX Cart."  
    fig6.data[4].name = "IX Bed." 
    fig6.data[5].name = "SBI" 
    fig6.data[6].name = "Sub-micron Filter" 
    fig6.update_layout(legend_x=0.02, legend_y=0.98)


    mabr_l = int(x_l[-1,0]*100/8712.2)
    acc_l = int(x_l[-1,-1]*100/8712.2)

    rul_1 = 'RUL (% Health): '+ rul_1
    rul_2 = 'RUL (Liters): ' + rul_2
    rul_3 = 'RUL (%): ' + str(round(KH_l[-1,1]*100/(KH_l[0,1]),1))
    rul_4 = 'RUL (Liters): ' + str(round(KH_l[-1,1],0))
    
    FR_str = str(round(np.mean(y_l[-1000:-1,4])*1000*3600,1))
    
    FR = 'Production Rate (LPH): ' + FR_str
    
    
    In_cond = "Inlet Water Conductivity (uS/cm):" + str(round(np.mean(k_l[-1000:-1,0]),1))
    p_ix_cond = 'Post IX Conductivity (uS/cm): ' + str(round(np.mean(k_l[-1000:-1,9]),1))
    Out_cond = 'Product Water Conductivity: (uS/cm): ' + str(round(np.mean(k_l[-1000:-1,15]),1))

    return fig1, fig3, fig4, fig5, fig6, mabr_l, acc_l, rul_1, rul_2, rul_3, rul_4, 'WRS Pump Status: ON', FR, In_cond, p_ix_cond, Out_cond


# if __name__ == '__main__':
    
#     app.run_server(debug=True)
# #     app.run_server(debug=False, host="0.0.0.0", port = 5010)
