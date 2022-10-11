from . Params import *
import numpy as np
import random

# def sim_time_split(sim_time_sec):
    
#     quo, rem = divmod(sim_time_sec, 1000)

#     return quo, rem

def WW_K_bounds() : # upper and lower bounds for inlet water 
    lower_bound = 50
    upper_bound = 1500

    return lower_bound, upper_bound
    
def bounded_random_walk(length, lower_bound, upper_bound, start, end, std):

# https://stackoverflow.com/questions/46954510/random-walk-series-between-start-end-values-and-within-minimum-maximum-limits

    assert (lower_bound <= start and lower_bound <= end)
    assert (start <= upper_bound and end <= upper_bound)

    bounds = upper_bound - lower_bound

    rand = (std * (np.random.random(length) - 0.5)).cumsum()
    rand_trend = np.linspace(rand[0], rand[-1], length)
    rand_deltas = (rand - rand_trend)
    rand_deltas /= np.max([1, (rand_deltas.max()-rand_deltas.min())/bounds])

    trend_line = np.linspace(start, end, length)
    upper_bound_delta = upper_bound - trend_line
    lower_bound_delta = lower_bound - trend_line

    upper_slips_mask = (rand_deltas-upper_bound_delta) >= 0
    upper_deltas =  rand_deltas - upper_bound_delta
    rand_deltas[upper_slips_mask] = (upper_bound_delta - upper_deltas)[upper_slips_mask]

    lower_slips_mask = (lower_bound_delta-rand_deltas) >= 0
    lower_deltas =  lower_bound_delta - rand_deltas
    rand_deltas[lower_slips_mask] = (lower_bound_delta + lower_deltas)[lower_slips_mask]

    return trend_line + rand_deltas


def start_end():
    
    lower_bound, upper_bound = WW_K_bounds() # waster water conductivity bounds
#     start = lower_bound + random.random() *(upper_bound - lower_bound)
#     end   = lower_bound + random.random() *(upper_bound - lower_bound)
    start = lower_bound + np.random.beta(1.5, 5, size=None) *(upper_bound - lower_bound)
    end   = lower_bound + np.random.beta(1.5, 5, size=None) *(upper_bound - lower_bound)
    
    return start, end

def gen_WW_Ks(sim_sec, start = start_end()[0]) : # Generate Waste water conductivity values
    
#     print(start)
    len_repeat = 1000
    
    assert(sim_sec >= len_repeat)

    quo, rem = divmod(sim_sec, len_repeat)
    
    lower_bound, upper_bound = WW_K_bounds() # waster water conductivity bounds
    
    end = start_end()[1]
    
    WW_k_data = np.zeros(sim_sec) # initiating the returned array of k values for waste water
        
    for i in range(quo) :
        
        random_data = bounded_random_walk(len_repeat, lower_bound, upper_bound, start, end, std=30)

        WW_k_data[i*len_repeat:(i+1)*len_repeat] = random_data
        
        start = random_data[-1]
        
        end = lower_bound + np.random.beta(1.5, 5, size=None) *(upper_bound - lower_bound)
        
    if rem>0:
        
        end = start + end* (rem/len_repeat) # To prevent sharp changes in WW k values when the rem is very small

        WW_k_data[(i+1)*len_repeat : sim_sec] = bounded_random_walk(rem, lower_bound, upper_bound, start, end, std=30)

    return WW_k_data
    


# random_data = bounded_random_walk(rem, lower_bound=50, upper_bound =100, start=50, end=100, std=10)
