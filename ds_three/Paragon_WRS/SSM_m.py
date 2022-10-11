# WRS state-space model to calculate and update flows, pressures, and EC states at different locations in the WRS. Also has control logic to turn on/off pump and to keep tanks at half state. 

import numpy as np
import pandas as pd
from . Params import *
from . Degradation import *


def wrs_m(x,y,k,Q,KH,KC,FR,u,d_c) :  # Paragon WRS. State space model. Advances state space model by 1 second when called.

    tank_pres = tank_capacity()
    
# unpacking pressure states
    p_mbr     = x[0] # MABR as a tank's head pressre
    p_p1      = x[1] # Pipe 1 internal pressure
    p_pump1   = x[2] # Pump 1 head pressure
    p_p2      = x[3] # Pipe 2 internal pressure
    p_f1      = x[4] # Pressure across Filter 1
    p_p3      = x[5] # Pipe 3 internal pressure
    p_f2      = x[6] # Pressure across activated carbon cartridge
    p_p4      = x[7] # Pipe 4 internal pressure
    p_f3      = x[8] # Pressure across Filter 2
    p_p5      = x[9] # Pipe 4 internal pressure
    p_f4      = x[10] # Pressure across Filter 3
    p_p6      = x[11] # Pipe 5 internal pressure
    p_s1      = x[12] # Pressure across silver biocide injector 1
    p_p7      = x[13] # Pipe 6 internal pressure
    p_f5      = x[14] # Pressure across Filter 4
    p_p8      = x[15] # Pipe 7 internal pressure
    p_acc     = x[16] # Accumulator Tank for potable water

# unpacking flow-rate states 
    q_in      = y[0] # Flow rate into MABR
    q_mabr    = y[1]  # MABR tank
    q_pump1   = y[2] # Pump 1 flow rate
    q_f1      = y[3] # filter 1
    q_f2      = y[4] # filter 2
    q_f3      = y[5] # filter 3
    q_f4      = y[6] # filter 3
    q_s1      = y[7] # silver biocide injector 1
    q_f5      = y[8] # filter 4
    q_acc     = y[9] # accumulator tank 
    q_out     = y[10] # for usage
    
    
# unpacking conductivity states
    k_in      = k[0]  # K before MABR
    k_mbr     = k[1] # K reduction across MABR
    k_p1      = k[2]  # K in Pipe 1
    k_p2      = k[3]  # K in Pipe 2
    k_f1      = k[4]  # K reduction Filter 1
    k_p3      = k[5]  # K in Pipe 3
    k_f2      = k[6]  # K reduction Filter 2
    k_p4      = k[7]  # K in Pipe 4    
    k_f3      = k[8]  # K reduction Filter 3
    k_p5      = k[9]  # K in Pipe 4
    k_f4      = k[10]  # K reduction Filter 4
    k_p6      = k[11]  # K in Pipe 5
    k_s1      = k[12]  # K reduction silver biocide injector 1
    k_p7      = k[13] # K in Pipe 6
    k_f5      = k[14] # K reduction across Filter 5
    k_p8      = k[15] # K in Pipe 7

    
# unpacking cumulative-flow states
    Q_MABR    = Q[0] # MABR tank
    Q_pump1   = Q[1] # Pump 1 flow rate
    Q_f1      = Q[2] # filter 1
    Q_f2      = Q[3] # filter 2
    Q_f3      = Q[4] # filter 2
    Q_f4      = Q[5] # filter 3
    Q_s1      = Q[6] # silver biocide injector 1
    Q_f5      = Q[7] # filter 4   
    
# Filter/Component Capacity/Health in liters - KH
    KH_MABR    = KH[0]  # MABR
    KH_f1      = KH[1]  # Filter 1 
    KH_f2      = KH[2]  # Filter 2
    KH_f3      = KH[3]  # Filter 2 
    KH_f4      = KH[4]  # Filter 3 
    KH_s1      = KH[5]  # Silver biocide injector 
    KH_f5      = KH[6]  # Filter 4 
    
# Unpacking Conductivity Conductance percentage - KH
    KC_mbr     = KC[0]  # MABR
    KC_f1      = KC[1]  # Filter 1 
    KC_f2      = KC[2]  # Filter 2 
    KC_f3      = KC[3]  # Filter 2 
    KC_f4      = KC[4]  # Filter 3 
    KC_s1      = KC[5]  # Silver biocide injector 
    KC_f5      = KC[6]  # Filter 4 
    
# Flow Coefficient
    FR_pump   = FR[0]
    FR_f1     = FR[1]
    FR_f2     = FR[2]
    FR_f3     = FR[3]
    FR_f4     = FR[4]
    FR_s1     = FR[5]
    FR_f5     = FR[6]
    FRD_f1_var = FR[7]
    
# unpacking control states
    u_pump1  = u[0] # pump 1
    p_1 = 20 # Pump 1 head pressure
    p_pump1 = p_1 * 6895  # psi -> Pa
    
# Component capacitance. Indicative of volume/Cross sectional area
    C_mbr, C_acc, C_f1, C_f2, C_f3, C_f4, C_s1, C_f5 = Capacitance_constants() 

# Calculating new Pressure states    
    p_mbr    =   ((1/(C_mbr)) * (q_in - q_pump1)) + p_mbr  ## the values are being updated   
    p_p1  = p_mbr # Directly connected to tank
    
    p_pump1 = p_pump1 + (p_pump1) * (0.1 * np.random.normal(0,1)) # Adding noise to pump pressure
    p_p2 =   ((1/(C_f1)) * (q_pump1 - q_f1)) + p_p2
    p_p3 =   ((1/(C_f2)) * (q_f1 - q_f2)) + p_p3
    p_p4 =   ((1/(C_f3)) * (q_f2 - q_f3)) + p_p4
    p_p5 =   ((1/(C_f4)) * (q_f3 - q_f4)) + p_p5
    p_p6 =   ((1/(C_s1)) * (q_f4 - q_s1)) + p_p6
    p_p7 =   ((1/(C_f5)) * (q_s1 - q_f5)) + p_p7
    p_acc =  ((1/(C_acc)) * (q_f5 - q_out)) + p_acc  ## the values are being updated
    p_p8 = p_acc
    
    p_f1 = p_p2 - p_p3  # Pressure drop across fijlters
    p_f2 = p_p3 - p_p4
    p_f3 = p_p4 - p_p5
    p_f4 = p_p5 - p_p6
    p_s1 = p_p6 - p_p7
    p_f4 = p_p7 - p_p8

    if p_mbr <= 0.5 * tank_pres:
        p_mbr = tank_pres/2

    if p_acc >= 0.5 * tank_pres:
        p_acc = tank_pres/2        
    
    if u_pump1 ==1 and (p_acc >= 0.95 * tank_pres or p_mbr <= 0.05 * tank_pres):
        u_pump1 = 0
    elif u_pump1 == 0 and p_mbr >= 0.5 * tank_pres:
        u_pump1 = 1
            
# Conductivity state updates
    k_p1      = k_in * KC_mbr # K in Pipe 1
    k_p2      = k_p1          # K in Pipe 2
    k_p3      = k_p2 * KC_f1  # K in Pipe 3
    k_p4      = k_p3 * KC_f2  # K in Pipe 4
    k_p5      = k_p4 * KC_f3  # K in Pipe 5
    k_p6      = k_p5 * KC_f4  # K in Pipe 6
    k_p7      = k_p6 * KC_s1  # K in Pipe 7
    k_p8      = k_p7 * KC_f5  # K in Pipe 8

    k_mbr     = k_in - k_p1  # K reduction across MABR
    k_f1      = k_p2 - k_p3  # K reduction/absorbed by Filter 1
    k_f2      = k_p3 - k_p4  # K reduction Filter 2  
    k_f3      = k_p4 - k_p5  # K reduction Filter 3
    k_f4      = k_p5 - k_p6  # K reduction across Filter 4
    k_s1      = k_p6 - k_p7  # K reduction silver biocide injector 1
    k_f5      = k_p7 - k_p8  # K reduction across Filter 5

    
# Flow rate updates      
    q_pump1  = u_pump1 * (FR_pump*np.sqrt(abs(p_mbr + p_pump1 - p_f1))) * np.sign(p_mbr + p_pump1 - p_f1) # Pump 1 flow rate
    q_f1  = FR_f1 * np.sqrt(abs(p_p2 - p_p3)) * np.sign(p_p2 - p_p3)                                       # Filter 1 flow rate
    q_f2  = FR_f2 * np.sqrt(abs(p_p3 - p_p4)) * np.sign(p_p3 - p_p4)
    q_f3  = FR_f3 * np.sqrt(abs(p_p4 - p_p5)) * np.sign(p_p4 - p_p5)
    q_f4  = FR_f4 * np.sqrt(abs(p_p5 - p_p6)) * np.sign(p_p5 - p_p6)
    q_s1  = FR_s1 * np.sqrt(abs(p_p6 - p_p7)) * np.sign(p_p6 - p_p7)
    q_f5  = FR_f5 * np.sqrt(abs(p_p7 - p_p8)) * np.sign(p_p7 - p_p8)
    
# Cumulative Flow through component updates
    Q_pump1   = Q_pump1 + q_pump1
    Q_f1      = Q_f1 + q_f1   # filter 1
    Q_f2      = Q_f2 + q_f2   # filter 2
    Q_f3      = Q_f3 + q_f3   # filter 3
    Q_f4      = Q_f4 + q_f4   # filter 4
    Q_s1      = Q_s1 + q_s1   # silver biocide injector 1
    Q_f5      = Q_f5 + q_f5   # filter 5
    
# RUL based on liters filtered. (Mfg.s recommendation probably)

    KH_MABR    = KH_MABR - q_pump1
    KH_f1      = KH_f1 - q_f1  # Filter 1 
    KH_f2      = KH_f2 - q_f2  # Filter 2 
    KH_f3      = KH_f3 - q_f3  # Filter 3
    KH_f4      = KH_f4 - q_f4  # Filter 4
    KH_s1      = KH_s1 - q_s1  # Silver biocide injector 
    KH_f5      = KH_f5 - q_f5  # Filter 5
    
# Conductivity filtering health/capacity.
    KC_new = KC # initiating KC_new. Updated below.
    
    if d_c[2] == True: # Control input from Dash UI. Degradation of Conductivity health.
        if d_c[4] == "Lin": # Linear degradation mode. Control input from Dash UI.
            KC_new = K_cond_upd(KC,y)
        else : # Advanced degradation mode
            KC_new = K_cond_upd_adv(KC, y, k)
            
# Filter 1 Clogging Health
    FR_new = FR # Initiating FR_new. Updated in the below code.

    if d_c[1] == True: # control input form Dash UI.    Filter degradation.    
        if d_c[3] == "Lin" : # Linear degradation of R
            FR_new = FR_upd(FR,y)
        else : # Advanced deg. mode. Depends on input water conductivity.
            FR_new = FR_upd_adv(FR, y, k)
            

# Updating states
    #x  = [  0 ,  1 ,    2  ,  3  , 4 ,  5  , 6  , 7  , 8  , 9  , 10 , 11 , 12 , 13 , 14 , 15 , 16  ]
    x   = [p_mbr,p_p1,p_pump1,p_p2,p_f1,p_p3,p_f2,p_p4,p_f3,p_p5,p_f4,p_p6,p_s1,p_p7,p_f5,p_p8,p_acc]
    
    #y  = [  0  ,   1 ,   2     ,   3 ,   4 ,  5  , 6   ,   7 ,   8 ,   9  ,  10]
    y   = [q_in, q_mabr, q_pump1, q_f1, q_f2, q_f3, q_f4, q_s1, q_f4, q_acc, q_out]
    
    #k  =  [  0 ,  1  ,  2   ,  3  ,  4  ,  5  ,  6  ,  7  ,  8  ,  9  ,  10 ,  11 ,  12 ,  13 ,  14 ,  15 ]    
    k   =  [k_in, k_mbr, k_p1, k_p2, k_f1, k_p3, k_f2, k_p4, k_f3, k_p5, k_f4, k_p6, k_s1, k_p7, k_f5, k_p8]
    
    #y  = [  0   ,    1   ,   2 ,   3 ,   4 ,  5  ,   6 ,  7  ]
    Q   = [Q_MABR, Q_pump1, Q_f1, Q_f2, Q_f3, Q_f4, Q_s1, Q_f5]
    
    KH = [KH_MABR, KH_f1, KH_f2, KH_f3, KH_f4, KH_s1, KH_f5]
    
    KC = KC_new 
#     KC = [KC_mbr, KC_f1, KC_f2, KC_f3, KC_s1, KC_f4]
    
    FR = FR_new
#     FR = [FR_pump, FR_f1, FR_f2, FR_f3, FR_s1, FR_f4]
    
    u   = [u_pump1] 
    
    return x, y, k, Q, KH, KC, FR, u
