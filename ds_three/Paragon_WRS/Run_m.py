# Function to run WRS state space model for the length of simulation, store variables and output them as arrays and data frames.

import numpy as np
import pandas as pd
from . SSM_m import *
from . Params import *
from . WW_Emulator import *

def run_wrs_m(run_time_hrs, d_ctrls) : # run_hours , controls from dash
    # function to run WRS state space model in loop and save states for plotting.

    num_seconds = int(60 * 60 * run_time_hrs) # 1 hour in seconds. No. of simulation steps
    
    tank_pres = tank_capacity()
    
#     if ersatz() == True: # If the gray water conductivity is controlled. Control added to dash UI. Deprecated.
#         WW_ks[:] = 200

    if d_ctrls[0] == "const":
        WW_ks = np.ones(num_seconds) * 200
    else :
        WW_ks = gen_WW_Ks(num_seconds) # conductivity of waste water simulated/measured for the length of simulation

    k_WW_in = WW_ks[0]
    
    x_in   =  [tank_pres,0,20,0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0] # Initial Pressure states
    y_in   =  [0, 0, 0,0,0,0,0,0,0,0,0] # Initial flow rate states
    k_in   =  [k_WW_in,0,0, 0, 0,0,0,0,0,0,0,0,0,0,0,0] # conductivity states
    Q_in   =  [0,0,0,0,0,0,0,0] # Cumulative through water flow
    KH_in  =  filter_k_capacitance()     # Filter health as measured by No. of liters filtering capacity
    KC_in  =  K_Conductance_constants()  # [KC_mbr, KC_f1, KC_f2, KC_f3, KC_s1, KC_f4]
    u_in   =  [1] #  Initial pump controls. Pump is always on.
    FR_in  =  Flow_Resistivity_constants()    # R_pump1, R_f1, R_f2, R_f3, R_s1, R_f4

    ### - Running the first step and storing the outputs to the initialized lists.
    
    x_i,y_i,k_i,Q_i,KH_i,KC_i,FR_i,u_i = wrs_m(x_in,y_in,k_in,Q_in,KH_in,KC_in,FR_in,u_in,d_ctrls) # "wrs" function from "Simulation" module
    
    ### - Initializing empty lists before running simulation. 
    
    x_list   =  []
    y_list   =  []
    k_list   =  []
    Q_list   =  []
    KH_list  =  []
    KC_list  =  []
    FR_list  =  []
    u_list   =  []

    x_list.append(x_i) # Appending/ storing values to the lists.
    y_list.append(y_i)
    k_list.append(k_i)
    Q_list.append(Q_i)
    KH_list.append(KH_i)
    KC_list.append(KC_i)
    FR_list.append(FR_i)
    u_list.append(u_i)

### - Running the remaining steps of the simulation and storing the outputs in each step.
    
    for i in range(1,num_seconds): 
        
        k_i[0] =  WW_ks[i]
              
        x_i,y_i,k_i,Q_i,KH_i,KC_i,FR_i,u_i = wrs_m(x_i,y_i,k_i,Q_i,KH_i,KC_i,FR_i,u_i,d_ctrls) # wrs fun call
        
        x_list.append(x_i) # Appending/ storing values to the lists.
        y_list.append(y_i)
        k_list.append(k_i)
        Q_list.append(Q_i)
        KH_list.append(KH_i)
        KC_list.append(KC_i)
        FR_list.append(FR_i)
        u_list.append(u_i)
      
### - Converting lists to arrays
    
    x_list = np.array(x_list)
    y_list = np.array(y_list) #* 1000*60*60
    k_list = np.array(k_list)
    Q_list = np.array(Q_list) #* 1000
    KH_list = np.array(KH_list) * 1000  
    KC_list = np.array(KC_list)
    FR_list = np.array(FR_list)
    u_list = np.array(u_list)

    wrs_x = pd.DataFrame(x_list, columns= ['p_mbr','p_p1','p_pump1', 'p_p2','p_f1','p_p3','p_f2','p_p4','p_f3','p_p5','p_f4','p_p6','p_s1', 'p_p7','p_f5','p_p8','p_acc'])
    wrs_x['Time [min]'] = wrs_x.index /60
    wrs_x.set_index('Time [min]', inplace=True)

    wrs_y = pd.DataFrame(y_list, columns=['q_in', 'q_mabr', 'q_pump1', 'q_f1', 'q_f2', 'q_f3', 'q_f4', 'q_s1', 'q_f4', 'q_acc', 'q_out'])
    wrs_y['time(min)'] = wrs_y.index /60
    wrs_y.set_index('time(min)', inplace=True)

    wrs_k=pd.DataFrame(k_list,columns=['k_in','k_mbr','k_p1','k_p2','k_f1','k_p3','k_f2','k_p4','k_f3','k_p5','k_f4','k_p6','k_s1','k_p7','k_f5','k_p8'])
    wrs_k['time(min)'] = wrs_k.index /60
    wrs_k.set_index('time(min)', inplace=True)
  
    wrs_Q = pd.DataFrame(Q_list, columns=['Q_MABR','Q_pump1', 'Q_f1', 'Q_f2', 'Q_f3', 'Q_f4', 'Q_s1', 'Q_f5'])
    wrs_Q['time(min)'] = wrs_Q.index /60
    wrs_Q.set_index('time(min)', inplace=True)
    
    wrs_KH = pd.DataFrame(KH_list, columns=['MABR', 'Micron Filter', 'Carbon Cart.','IX Cart.','IX Bed','SBI','Sub-Micron Filter'])
    wrs_KH['time(min)'] = wrs_KH.index /60
    wrs_KH.set_index('time(min)', inplace=True)
    
    wrs_KC = pd.DataFrame(KC_list, columns=['KC_MABR','KC_f1','KC_f2','KC_f3','KC_f4','KC_s1','KC_f5'])
    wrs_KC['time(min)'] = wrs_KC.index /60
    wrs_KC.set_index('time(min)', inplace=True)
    
    wrs_FR = pd.DataFrame(FR_list, columns=['FR_pump','FR_f1','FR_f2','FR_f3','FR_f4', 'FR_s1','FR_f5', 'FRD_f1_var'])
    wrs_FR['time(min)'] = wrs_FR.index /60
    wrs_FR.set_index('time(min)', inplace=True)
    
    wrs_u = pd.DataFrame(u_list, columns=['u_pump1'])
    wrs_u['time(min)'] = wrs_u.index /60
    wrs_u.set_index('time(min)', inplace=True)

    return x_list,y_list,k_list,Q_list,KH_list,KC_list,FR_list,u_list, wrs_x,wrs_y,wrs_k,wrs_Q,wrs_KH,wrs_KC,wrs_FR,wrs_u 
