# Different functions to pull initial WRS parameters and degradation rate constants from.

from . SSM_m import *
from . Run_m import *

# Whether or not inlet water conductivity is constant. Probably deprecated function.
def ersatz():
    ersatz = False
    return ersatz

# Whether or not electric conductivity health degrades
def KC_degradation() :
    return True 

# Basic or Advanced electric conductivity health.
def KC_degradation_method() : 
    # "Basic" or "Adv"   
    return "Adv"

# Whether or not Filter clogging happens
def Filter_clog_degradation() : 
    return True  # True/ False

# Type of filter clog (permeability) degradation
def Filter_clog_degr_method() : # Basic or Advanced filter clogging
    # "Basic" or "Adv"   
    return "Adv"

# Tank capacity in head pressure.
def tank_capacity(): # Tank pressure when full.
    tank_pres = 8.7122e3 
    return tank_pres

# Mfg. recommended maximum volume (in m^3) of water that can be filtered by a component.
def filter_k_capacitance() : 
    KH_m = 10000 * 1e-3 # sample filter capacity in liters to m**3 of filters & catridges
    KH_in  =  [KH_m, KH_m, 2*KH_m, 2*KH_m, 1.5*KH_m, 0.75*KH_m, 1.25*KH_m]
    return KH_in

# Capacitance constants for different components. How much pressure changes for a given flow into a component.
def Capacitance_constants() : # indicates the pressure change for fluid accumulation. 
    C_mbr = 1.8614e-4  # MABR tank capacitance
    C_acc = 1.8614e-4  # Accumulator tank capacitance
    C_f1  = 9.1207e-6  # Filter 1 capacitance
    C_f2  = 9.1207e-6  # Filter 2 capacitance
    C_f3  = 9.1207e-6  # Filter 3 capacitance
    C_f4  = 9.1207e-6  # Filter 4 capacitanceQ
    C_s1  = 9.1207e-6  # Silver biocide injector capacitance
    C_f5  = 9.1207e-6  # Filter 4 capacitance 
    return C_mbr, C_acc, C_f1, C_f2, C_f3, C_f4, C_s1, C_f5

# To vary filter permeability delta for Filter-1 in each simulation.
def FR_Deg_f1_var(sims = None):
    FRD_f1_var = (np.random.beta(10, 10, size=sims) - 0.5) * 50/100  # 50 % variation in FRD_f1 value
    return FRD_f1_var

# Flow resitiviy constants - How much resistance/inverse do these components offer to flow
def Flow_Resistivity_constants() : # Flow resistivity. Actually inverse of flow resistivity. Initial values.
    FR_pump1   = 1.0000e-7  # Flow conductance
    FR_f1      = 1.5000e-6  # Filter 1 conductance
    FR_f2      = 1.5000e-6 * 2 # Filter 2 conductance
    FR_f3      = 1.5000e-6 * 3  # Filter 3 conductance
    FR_f4      = 1.5000e-6 * 10  # Filter 4 conductance
    FR_s1      = 1.5000e-6  # Silver biocide injector conductance
    FR_f5      = 1.5000e-6 * 10  # Filter 4 conductance
    FRD_f1_var = FR_Deg_f1_var() # is called once at the beginning of the simulation. Then stays constant.
    return [FR_pump1, FR_f1, FR_f2, FR_f3, FR_f4, FR_s1, FR_f5, FRD_f1_var]

# Filter permeability degradation delta in each timestep.
def FR_const_degrad(FRD_f1_var):
    FRD_f1_mean      = 1.5000e-6 * 1e-4 * 1  # Filter 1 conductance. NEED TO VARY THIS IN MONTE CARLO SIMULATION
    FRD_f1 = FRD_f1_mean + FRD_f1_mean * FRD_f1_var  # varies x (20)% up and below the given mean value
    
    FRD_pump1   = 0  #1.0000e-7 * 1e-6 # Flow conductance
    FRD_f2      = 0  #1.5000e-6 * 1e-3  # Filter 1 conductance
    FRD_f3      = 0  # 1.5000e-6 * 1e-6  # Filter 2 conductance
    FRD_f4      = 0  # 1.5000e-6 * 1e-6  # Filter 3 conductance
    FRD_s1      = 0  # 1.5000e-6 * 1e-6  # Silver biocide injector conductance
    FRD_f5      = 0  # 1.5000e-6 * 1e-6  # Filter 4 conductance
    return [FRD_pump1, FRD_f1, FRD_f2, FRD_f3, FRD_f4, FRD_s1, FRD_f5]

# Filter permeability failure threshold value.
def Filter_Fail_Threshold(): # for micron filter.
    fail_value = (Flow_Resistivity_constants()[1]) * 2/3
    return fail_value

# Conductivity conductance constants - How much conductivity causing particles do these components let through.
def K_Conductance_constants() :  # Initial K_conductance_constants
    KC_mbr  = 0.9 
    KC_f1   = 0.9
    KC_f2   = 0.9
    KC_f3   = 0.1
    KC_f4   = 0.2
    KC_s1   = 0.8
    KC_f5   = 0.8
    return [KC_mbr, KC_f1, KC_f2, KC_f3, KC_f4, KC_s1, KC_f5]

# K_conductance_constants degradation factor in each step.
def K_Cond_const_degrad(): 
    KCD_mbr  = 0.9*1e-3
    KCD_f1   = 0.9*1e-3
    KCD_f2   = 0.9*1e-3
    KCD_f3   = (0.1*1e-3) *5
    KCD_f4   = 0.2*1e-3
    KCD_s1   = (0.8*1e-4)*3
    KCD_f5   = (0.8*1e-3)*2
    return [KCD_mbr, KCD_f1, KCD_f2, KCD_f3, KCD_f4, KCD_s1, KCD_f5]
