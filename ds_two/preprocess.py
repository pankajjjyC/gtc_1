# V4 - 6/9/2022 J. Williams
# Updated so packages are only loaded when function is called
# 
# V3  -  8/19/2021  L. Barama
# Added extra dimension to the get_amplitudes function to avoid ValueError 
# when trying to run process_wave function
# 
# V2 - 7/21/2021
# Added full preprocessing method.
# The input is a three component waveform
# The output is a unified feature vector
#
# V1 - 5/6/2021
# Copied over from pywave

import numpy as np


def get_amplitudes(waves):
    """Used for multiple waves"""
    waves = np.abs(waves)
    amplitudes = waves.max(axis=1)
    amplitudes = np.expand_dims(amplitudes, axis=-1) # Add an extra dimension in the last axis. kept getting error of : "ValueError: operands could not be broadcast together with shapes (6045,600) and (6045,) of output of process_waves function
    
    return amplitudes


def detrend(wave):
    """Removes a linear trend from the wave"""

    x = np.arange(len(wave))
    slope, intercept = np.polyfit(x, wave, 1)
    lin_fit = slope * x + intercept
    wave_detrend = wave - lin_fit
    return wave_detrend


def taper(wave, taper_fraction=0.05): 
    """ taper_fraction is the amount on the start and end. total taper is twice as much.
    """
    taper_length = int(len(wave) * taper_fraction)
    # Build the start tapper
    taper_range = np.arange(taper_length)
    taper_start = np.sin(taper_range/taper_length*np.pi/2)
    # Build the end tapper
    taper_end = np.sin(np.pi/2 + taper_range/taper_length*np.pi/2)
    # Build a center section of only 1s
    taper_center = np.ones(len(wave)-2*taper_length)
    # Concatenate the start, center, and end
    taper_function = np.concatenate([taper_start,taper_center,taper_end])
    # Multiply the wave by the taper function
    wave = wave * taper_function
    return wave

def lowpass_filter(wave, lowpass_cutoff=4, sampling_rate=20, lowpass_order=4):
    """ Low pass filter using a butter-lowpass.
    The cutoff and sampling_rate parameters are in Hz.
    The order dictates the attenuation after the cutoff frequency.
    A low order has a long attenuation."""
    try:
        from scipy.signal import butter, lfilter, freqz
    except:
        return print('Cannot load scipy')

    nyq = 0.5 * sampling_rate
    normal_cutoff = lowpass_cutoff / nyq
    # TODO look for bandpass
    b, a = butter(lowpass_order, normal_cutoff, btype='low', analog=False)

    wave = lfilter(b, a, wave)

    return wave

def resample(wave, target_freq=20, window_seconds=30):
    from scipy.signal import decimate, resample
    n_resample_points = target_freq * window_seconds
    wave = resample(wave, n_resample_points)
    return wave


def highpass_filter(wave, highpass_cutoff=0.5, sampling_rate=20, highpass_order=4):
    """ High pass filter using a butter-lowpass.
    The cutoff and sampling_rate parameters are in Hz.
    The order dictates the attenuation after the cutoff frequency.
    A low order has a long attenuation.
    Ref website: https://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units"""
    try:
        from scipy.signal import butter, lfilter, freqz
    except:
        return print('Cannot load scipy')

    nyq = 0.5 * sampling_rate
    normal_cutoff = highpass_cutoff / nyq
    b, a = butter(highpass_order, normal_cutoff, btype='high', analog=False)

    wave = lfilter(b, a, wave)

    return wave

def bandpass_filter(wave, lowpass_cutoff=0.5, highpass_cutoff=8, sampling_rate=20, order=4):
    """ Band pass filter using a butter-lowpass.
    The cutoff and sampling_rate parameters are in Hz.
    The order dictates the attenuation after the cutoff frequency.
    A low order has a long attenuation."""

    try:
        from scipy.signal import butter, lfilter, freqz
    except:
        return print('Cannot load scipy')

    pass_band = [lowpass_cutoff, highpass_cutoff]

    b, a = butter(N=order, Wn=pass_band, btype='bandpass', analog=False, fs=sampling_rate)

    wave = lfilter(b, a, wave)

    return wave


############
# Old Code #
############

def process_waves(waves, sampling_rates):
    """ Iteratively process all waves and return a numpy array and an amplitude array
    """
    import matplotlib.pyplot as plt

    # Instance a list to hold the processed waves
    processed_waves = []

    # Iterate through the waves as long as they are different lengths
    for idx, wave in enumerate(waves):
        sampling_rate = sampling_rates[idx]

        # Detrend
        wave = detrend(wave)

        # Taper: 5% (2.5 and 2.5)
        # TODO 10% (5% and 5%)
        wave = taper(wave,taper_fraction=0.05)

        # Low pass filter: 10Hz (Low pass filter must be less than half of sampling rate)
        wave = lowpass_filter(wave, lowpass_cutoff=9, sampling_rate=sampling_rate)

        # Resample: 20Hz
        wave = resample(wave)

        # Append wave to list
        processed_waves.append(wave)

    # Convert process waves to np array
    processed_waves = np.array(processed_waves)

    # Band pass: 0.5 - 8Hz
    processed_waves = highpass_filter(processed_waves, highpass_cutoff=0.5)
    processed_waves = lowpass_filter(processed_waves, lowpass_cutoff=8)

    # Get amplitudes
    amplitudes = get_amplitudes(processed_waves)

    # Normalize
    processed_waves = processed_waves/amplitudes

    # Return waves (numpy array) and amplitudes (numpy array)
    return processed_waves, amplitudes

def process_waves_no_normalization(waves, sampling_rates):
    """ Iteratively process all waves and return a numpy array and an amplitude array
    """
    import matplotlib.pyplot as plt

    # Instance a list to hold the processed waves
    processed_waves = []

    # Iterate through the waves as long as they are different lengths
    for idx, wave in enumerate(waves):
        sampling_rate = sampling_rates[idx]

        # Detrend
        wave = detrend(wave)

        # Taper: 5% (2.5 and 2.5)
        # TODO 10% (5% and 5%)
        wave = taper(wave,taper_fraction=0.05)

        # Low pass filter: 10Hz (Low pass filter must be less than half of sampling rate)
        wave = lowpass_filter(wave, lowpass_cutoff=9, sampling_rate=sampling_rate)

        # Resample: 20Hz
        wave = resample(wave)

        # Append wave to list
        processed_waves.append(wave)

    # Convert process waves to np array
    processed_waves = np.array(processed_waves)

    # Band pass: 0.5 - 8Hz
    processed_waves = highpass_filter(processed_waves, highpass_cutoff=0.5)
    processed_waves = lowpass_filter(processed_waves, lowpass_cutoff=8)

    # Return waves (numpy array) and amplitudes (numpy array)
    return processed_waves

def process_waves_for_autoencoder(waves, sampling_rates):
    """ Iteratively process all waves and return a numpy array and an amplitude array
    """
    import matplotlib.pyplot as plt

    # Instance a list to hold the processed waves
    processed_waves = []

    # Iterate through the waves as long as they are different lengths
    for idx, wave in enumerate(waves):
        sampling_rate = sampling_rates[idx]

        # Detrend
        wave = detrend(wave)

        # Taper: 5% (2.5 and 2.5)
        # TODO 10% (5% and 5%)
        wave = taper(wave)

        # Low pass filter: 10Hz (Low pass filter must be less than half of sampling rate)
        wave = lowpass_filter(wave, lowpass_cutoff=9, sampling_rate=sampling_rate)

        # Resample: 20Hz
        wave = resample(wave)

        # Append wave to list
        processed_waves.append(wave)

    # Convert process waves to np array
    processed_waves = np.array(processed_waves)

    # Band pass: 0.5 - 8Hz
    processed_waves = bandpass_filter(wave, lowpass_cutoff=0.5, highpass_cutoff=8, sampling_rate=20, order=4)

    # Get amplitudes
    amplitudes = get_amplitudes(processed_waves)

    # Normalize
    processed_waves = processed_waves/amplitudes

    # Return waves (numpy array) and amplitudes (numpy array)
    return processed_waves, amplitudes

# Old function from pywave
def process_data(dataset,sampling_rate=40,decimals=3, # General inputs
    taper_fraction=0.1, # taper function inputs
    highpass_cutoff=1,highpass_order=4, # high pass filter inputs
    lowpass_cutoff=4, lowpass_order=4): # low pass filter inputs
    """Processes a dataset of shape (n_observations, n_channels, n_readings)
    For each wave it applies:
    centering -> taper -> highpass -> lowpass"""
    
    # By copying the dataset, the orginal dataset will remain unaltered
    dataset = dataset.copy()

    # Process data by each observation and wave
    for idx, observation in enumerate(dataset):
        channel0 = observation[0]
        channel0 = center(channel0)
        channel0 = taper(channel0, taper_fraction)
        channel0 = highpass_filter(channel0, highpass_cutoff, sampling_rate, highpass_order)
        channel0 = lowpass_filter(channel0, lowpass_cutoff, sampling_rate, lowpass_order)
        dataset[idx][0] = channel0
        
        channel1 = observation[1]
        channel1 = center(channel1)
        channel1 = taper(channel1, taper_fraction)
        channel1 = highpass_filter(channel1, highpass_cutoff, sampling_rate, highpass_order)
        channel1 = lowpass_filter(channel1, lowpass_cutoff, sampling_rate, lowpass_order)
        dataset[idx][1] = channel1
        
        channel2 = observation[2]
        channel2 = center(channel2)
        channel2 = taper(channel2, taper_fraction)
        channel2 = highpass_filter(channel2, highpass_cutoff, sampling_rate, highpass_order)
        channel2 = lowpass_filter(channel2, lowpass_cutoff, sampling_rate, lowpass_order)
        dataset[idx][2] = channel2

    # Round the dataset to reduce the size of the array
    #dataset = np.around(dataset,decimals=decimals)
    
    return dataset



def center(wave):
    """Centers the wave based on the mean"""
    wave = wave - wave.mean()
    return wave


def soft_clip(data, k=0.001):
    """Scales down data to make sizes of similar magnitude"""
    data = 1/(1+np.exp(-k * data))
    return data

def scale_by_varience(data, decimals=3):
    """Reduces sample by deviding by the varience of every wave"""
    data = data.copy()

    for idx, observation in enumerate(data):
        channel0 = observation[0]
        channel0 = channel0/(np.var(channel0)**0.5)
        data[idx][0] = channel0
        
        channel1 = observation[1]
        channel1 = channel1/(np.var(channel1)**0.5)
        data[idx][1] = channel1
        
        channel2 = observation[2]
        channel2 = channel2/(np.var(channel2)**0.5)
        data[idx][2] = channel2

    data = np.around(data,decimals=decimals)
    
    return data   

def shuffle_data(dataset, labels):
    """Shuffles the dataset and labels to randomize them for training"""
    indexes = np.arange(len(labels))
    np.random.shuffle(indexes) # in this case inplace=True

    # Make holding lists
    samples_shuffled = []
    labels_shuffled = []

    for index_shuffled in indexes:
        wave = dataset[index_shuffled]
        label = labels[index_shuffled]

        samples_shuffled.append(wave)
        labels_shuffled.append(label)

    samples_shuffled = np.array(samples_shuffled)
    labels_shuffled = np.array(labels_shuffled)

    return samples_shuffled, labels_shuffled

def reshape_data(dataset):
    """Takes dataset of (n_observations, n_channels, n_readings)
    and returns (n_observations, n_readings, n_channels)"""
    reshape_sample = np.array([sample.T for sample in dataset])
    return reshape_sample