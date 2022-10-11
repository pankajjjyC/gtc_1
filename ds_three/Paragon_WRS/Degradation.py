# Functions to degrade/update flow permeability values and filter electrical conductivity health values of components in WRS after each time step. These functions are called if degradation is turned on.

from . Params import *
from operator import add, sub
import numpy as np

# Updates flow permeability using basic method. Update depends on a constant, degradation delta, and flow rate in that timestep.
def FR_upd(FR,y) :
    FRD_f1_var = FR[7]
    FRD   = FR_const_degrad(FRD_f1_var) # flow permeability degradation amount for Filter 1
    FRD   = [element * 20 for element in FRD]
    y_frd = [y[2], y[3], y[4], y[5], y[6], y[7], y[8]]  
    FRDy = np.multiply(FRD, y_frd)
    FR_new = list(map(sub, FR, FRDy))
    FR_new = [0 if x<=0 else x for x in FR_new]
    FR_new.append(FRD_f1_var)
    return FR_new

# Updates flow permeability using advanced method. Update depends on a constant, degradation delta, EC experienced, and flow rate in that timestep.
def FR_upd_adv(FR, y, k) : # Current KC, y - flow rates, and k - conducvity states and amounts removed in by filters
    FRD_f1_var = FR[7]
    FRD = FR_const_degrad(FRD_f1_var)
    FRD = [element /20 for element in FRD]
#     FR_pump1   = FR[0] - y[2] * k[2]   * FRD[0] # Pump1. k[1] if filter in pipe 1. The k are the amounts of k filtered by components.
#     FR_f1      = FR[1] - y[3] * k[4]   * FRD[1] # Filter 1 
#     FR_f2      = FR[2] - y[4] * k[6]   * FRD[2] # Filter 2 
#     FR_f3      = FR[3] - y[5] * k[8]   * FRD[3] # Filter 3 
#     FR_f4      = FR[5] - y[6] * k[10]  * FRD[4] # Filter 4 
#     FR_s1      = FR[4] - y[7] * k[12]  * FRD[5] # Silver biocide injector 
#     FR_f5      = FR[5] - y[8] * k[14]  * FRD[6] # Filter 4 
    FR_pump1   = FR[0] - y[2] * k[2]   * FRD[0] # Pump1. k[1] if filter in pipe 1. The k are the amounts of k filtered by components.
    FR_f1      = FR[1] - y[3] * k[3]   * FRD[1] # Filter 1 
    FR_f2      = FR[2] - y[4] * k[5]   * FRD[2] # Filter 2 
    FR_f3      = FR[3] - y[5] * k[7]   * FRD[3] # Filter 3 
    FR_f4      = FR[5] - y[6] * k[9]  * FRD[4] # Filter 4 
    FR_s1      = FR[4] - y[7] * k[11]  * FRD[5] # Silver biocide injector 
    FR_f5      = FR[5] - y[8] * k[13]  * FRD[6] # Filter 4 
    FR_new = [FR_pump1, FR_f1, FR_f2, FR_f3, FR_f4, FR_s1, FR_f5]
    FR_new = [0 if x<=0 else x for x in FR_new]
    FR_new.append(FRD_f1_var)
    return FR_new

# Updates EC health using basic method. Update depends on a constant, degradation delta, and flow rate in that timestep.
def K_cond_upd(KC,y) : # Cartridge conductivity update
    KCD = K_Cond_const_degrad()
    KCD = [element * 20 for element in KCD]
    y_kcd = [y[1], y[3], y[4], y[5], y[6], y[7], y[8]]
    KCDy = np.multiply(KCD, y_kcd)
    KC_new = list( map(add, KC, KCDy))
    KC_new = [1 if x>=1 else x for x in KC_new]
    return KC_new

# Updates EC health using advanced method. Update depends on a constant, degradation delta, EC filtered, and flow rate in that timestep.
def K_cond_upd_adv(KC, y , k) : # Current KC, y - flow rates, and k - conducvity states and amounts removed in by filters
    KCD = K_Cond_const_degrad()
    KCD = [element /10 for element in KCD]
    KC_mbr     = KC[0] + y[1] * k[1]   *  KCD[0] # MABR
    KC_f1      = KC[1] + y[3] * k[4]   *  KCD[1] # Filter 1 
    KC_f2      = KC[2] + y[4] * k[6]   *  KCD[2] # Filter 2 
    KC_f3      = KC[3] + y[5] * k[8]   *  KCD[3] # Filter 3
    KC_f4      = KC[4] + y[6] * k[10]  *  KCD[4] # Filter 4 
    KC_s1      = KC[5] + y[7] * k[12]  *  KCD[5] # Silver biocide injector 
    KC_f5      = KC[6] + y[8] * k[14]  *  KCD[6] # Filter 4 
    KC_new = [KC_mbr, KC_f1, KC_f2, KC_f3, KC_f4, KC_s1, KC_f5]
    KC_new =  [1 if x>=1 else x for x in KC_new]
    return KC_new


