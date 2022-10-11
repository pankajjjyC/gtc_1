# Function to do one RUL simulation with fixed degradation rate constant.

import numpy as np
# import matplotlib.pyplot as plt
from . SSM_m import *
from .Params import *
from .WW_Emulator import*


# Function that determines RUL in time and liters filtered to failure. Tankes in current state and predicts states over prediction horizon.
def RUL_Fil(xl,yl,kl,Ql,KHl,KCl,FRl,ul,d_ctrls, Hr_RUL):
    
#     Ind = ul[:,0][ul[:,0]==1] # finding the time steps where pump is running
#     xl  = xl[Ind,:]
#     yl  = yl[Ind,:]
#     kl  = kl[Ind,:]
#     Ql  = Ql[Ind,:]
#     KHl = KHl[Ind,:]
#     KCl = KCl[Ind,:]
#     FRl = FRl[Ind,:]    
#     ul  = ul[Ind,:]
    
    N_sec = int(Hr_RUL*60*60)  # hours to seconds
    
    sub_samp = 600 # Every 600th second is sampled/recorded for plots
    
#     Creating inlet water conductivity values for the RUL horizon.
    if d_ctrls[0] == "const":
        WW_ks = np.ones(N_sec+1) * 200
    else :
        WW_ks = gen_WW_Ks(N_sec+1) # conductivity of waste water simulated/measured for the length of simulation

### - The last pressure, flow and component states. In other words, the current system state.
    
    x     = xl[-1] # x is a vector of pressure states in the last second of simulation
    y     = yl[-1]
    k     = kl[-1]
    Q     = Ql[-1]
    KH    = KHl[-1]
    KC    = KCl[-1]
    FR    = FRl[-1]
    u     = ul[-1]
    
    Q_init     = Q[2]  # This is the cumulative flow (Flow volume) through Filter-1 upto the current step .
        
# Initializing variables to store predicted values
#     xp = np.zeros(N_sec + 1)
#     yp = np.zeros(N_sec + 1)
#     up = np.zeros(N_sec + 1)
    kp = np.zeros(N_sec + 1) 
    Q_filter   = np.zeros(N_sec + 1)
    FHP = np.zeros(N_sec + 1)
    
     # This is the zeroeth time step (Last known state of WRS). Storing variables.
    i = 0
    kp[i] = k[0]
#     xp[i] = x[16]  # This is the pressure parameter being tracked. Is the last simulated value of the tracked parameter.
#     yp[i] = y[3]  # This is the last simulated flow rate of the tracked flow rate parameter.
    FHP[i]= FR[1]  # FR[1] is the flow conductivity of fijlter 1 which is the primary fijlter under consideration for PHM.
    Q_filter[i]  = Q[2] - Q_init # 0. Basically zero.

    xfail = False # Initializing with not yet failed parameters.
    yfail = False
        
    for i in range(1, N_sec+1): # Prediction horizon
        
        k[0] = WW_ks[i]
        
        x,y,k,Q,KH,KC,FR,u = wrs_m(x,y,k,Q,KH,KC,FR,u,d_ctrls)
        
#         xp[i] = x[16]  # This is the pressure parameter being tracked. Is the last simulated value of the tracked parameter.
#         yp[i] = y[3]  # This is the last simulated flow rate of the tracked flow rate parameter.

        kp[i] = k[0]
        FHP[i]= FR[1]  # FR[1] is the flow conductivity of fijlter 1 which is the primary fijlter under consideration for PHM.
        Q_filter[i]  = Q[2] - Q_init # 0. Basically zero.
        
    Q_Fil =  Q_filter[::sub_samp]
    kparam = kp[::sub_samp]
    Fil_HP= FHP[::sub_samp]
    
    FHP_thr = np.ones(len(Q_Fil))*(Filter_Fail_Threshold())

#     plt.figure(figsize=(8,5.5)) 
#     plt.plot(Ql[:,2]-Ql[-1,2], FRl[:,1], color="black")
#     plt.plot(Q_Fil, Fil_HP)
#     plt.plot(Q_Fil, FHP_thr)
    
    Indexes = [idx for idx, element in enumerate(FHP) if element < FHP_thr[0]]
    
    Time_2_fail = None
    Lit_2_fail = None
        
    if Indexes!= []:
        Time_2_fail = round(Indexes[0]/(60*60),1)
        print("Time to failure:", Time_2_fail, "Hours")
        Lit_2_fail = round(Q_filter[Indexes[0]]*1000,1)
        print("Liters to failure", Lit_2_fail, "Liters")
    else:
        print("Time and Liters to failure is greater than", Hr_RUL, " hours and", round(Q_filter[i]*1000,1), "Liters")

    return Q_Fil, Fil_HP, FHP_thr, Time_2_fail, Lit_2_fail

