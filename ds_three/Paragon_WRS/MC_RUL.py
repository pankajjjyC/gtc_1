# Functions to run Monte Carlo Analyses and plot flow permeability degradation over prediction horizon along with failure threshold. Gives RUL in time and cum. filtered flow.

import numpy as np
import matplotlib.pyplot as plt
from numpy import savetxt
from . SSM_m import *
from .Params import *
from .WW_Emulator import*


def MC_RUL_Fil(xl,yl,kl,Ql,KHl,KCl,FRl,ul,d_ctrls, Hr_RUL, No_Sims):

    N_sec = int(Hr_RUL*60*60)  # hours to seconds
    
    xfail = False # Initializing with not yet failed parameters.
    yfail = False
    
    sub_samp = 2*3600 # Every 2 hours, a sampled/recorded for plots
    
    Q_Fil_MC = np.zeros((No_Sims, int((N_sec+1)/sub_samp)+1 )) # To save cumulative flow (Q) to generate RUL vs Q plot for all simulations
    
    FHP_fil_MC = np.zeros((No_Sims, int((N_sec+1)/sub_samp)+1)) # To save Filter Flow conductivity (FHP) for RUL vs Q plot for all simulations
    FRD_fil_MC_check = np.zeros((No_Sims, int((N_sec+1)/sub_samp)+1)) # To save Filter Flow conductivity (FHP) for RUL vs Q plot for all simulations
      
    FRD_fil_MC = FR_Deg_f1_var(sims = No_Sims)   
    FRD_fil_MC[0] = FRl[-1, 7]

    for j in range(No_Sims) :
        print("Simulation #", j+1, " in progress")

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

        #     Creating inlet water conductivity values for the RUL horizon.
        if d_ctrls[0] == "const":
            WW_ks = np.ones(N_sec+1) * 200
        else :
            WW_ks = gen_WW_Ks(N_sec+1) # conductivity of waste water simulated/measured for the length of simulation

    # Initializing variables to store predicted values
        xp = np.zeros(N_sec + 1)
        yp = np.zeros(N_sec + 1)
        up = np.zeros(N_sec + 1)
        kp = np.zeros(N_sec + 1) 
        Q_filter   = np.zeros(N_sec + 1)
        FHP = np.zeros(N_sec + 1)
        FHP_delta = np.zeros(N_sec + 1)

         # This is the zeroeth time step (Last known state of WRS). Storing variables.
        i = 0
#         kp[i] = k[0]
#         up[i] = u[0]
#         xp[i] = x[16]  # This is the pressure parameter being tracked. Is the last simulated value of the tracked parameter.
#         yp[i] = y[3]  # This is the last simulated flow rate of the tracked flow rate parameter.\
#         FHP_delta[i]= FR[7]

        FHP[i]= FR[1]  # FR[1] is the flow conductivity of fijlter 1 which is the primary fijlter under consideration for PHM.

        Q_filter[i]  = Q[2] - Q_init # 0. Basically zero.
        FR[7] = FRD_fil_MC[j] # Giving new filter degradation rates in each simulation
        
        FHP_thr = np.ones(N_sec + 1)*(Filter_Fail_Threshold())

        for i in range(1, N_sec+1): # Prediction horizon

            k[0] = WW_ks[i]

            x,y,k,Q,KH,KC,FR,u = wrs_m(x,y,k,Q,KH,KC,FR,u,d_ctrls)
        
#             xp[i] = x[16]  # This is the pressure parameter being tracked. Is the last simulated value of the tracked parameter.
#             yp[i] = y[3]  # This is the last simulated flow rate of the tracked flow rate parameter.
#             up[i] = u[0]
#             kp[i] = k[0]
            Q_filter[i]  = Q[2] - Q_init # 0. Basically zero.
            FHP[i]= FR[1]  # FR[1] is the flow conductivity of fijlter 1 which is the primary fijlter under consideration for PHM.
#             FHP_delta[i] = FR[7]
            
#         print(Q_filter[::sub_samp].shape)

        Q_Fil_MC[j,:] = Q_filter[::sub_samp]
        FHP_fil_MC[j,:] = FHP[::sub_samp]
#         FRD_fil_MC_check[j,:] = FHP_delta[::sub_samp]

#         file_name = "MCData1/Sim"+str(j+1)+'.csv' To save each simulation data to a file. In case computer freezes.
#         savetxt(file_name, [Q_Fil_MC[j,:],FHP_fil_MC[j,:]], delimiter=',')

        plt.plot(Q_Fil_MC[j,:], FHP_fil_MC[j,:])

    plt.plot(Ql[:,2]-Ql[-1,2], FRl[:,1],color="black")        
    plt.plot(Q_filter, FHP_thr)
    plt.xlabel("Liters Filtered [Liters*1000]")
    plt.ylabel("Filter Health Parameter")

    return Q_Fil_MC, FHP_fil_MC, FRD_fil_MC_check
