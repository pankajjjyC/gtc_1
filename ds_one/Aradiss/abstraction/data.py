# ARADISS abstraction v0.1.1
# Global Technology Connection, Inc.
# 8/4/2022
#
# Contains functions for dataset loading, preprocessing
# DTW score calculation
# Correlation graph generation
# Ground truth and target parameter selection
# Creation of feature set and training data for learning models
# 7/22 -generate_featureset() - fixed indexing issue within buffer for rolling average

import numpy as np
import pandas as pd


### This should be restructured into different modules, one for data loading/processing, and one for correlations
def load_dataset(infile, skip_rows=0, delim=','):
    '''
    Returns processed data contained in .csv file as a pandas dataframe
    Removes all nan, inf, and static variables
    ------------
    Parameters:
        infile: name of dataset to be loaded
    ------------
    Returns:
        data: Pandas Dataframe of cleaned dataset
    '''
    data = pd.read_csv(infile, skiprows=skip_rows, sep=delim, encoding='latin-1')
    #data = pd.read_csv(infile, encoding='utf-8-sig')
    data = data.select_dtypes(exclude=['object'])

    data = drop_static_columns(data)
    data.interpolate(method='linear', limit_direction='forward', axis=0, inplace=True)
    # fill all invalid points
    data.replace(['NaN', 'NaT', 'inf', '-inf', np.inf, -np.inf], 0, inplace=True)
    data = data.fillna(0)
    data = drop_static_columns(data)
    data = data.reset_index(drop=True)
    return data


def drop_static_columns(data):
    '''
    Drops unchanging or static parameters from dataframe
    * Updated 8/4/22, now uses pandas.unique to drop cols with less than 2 unique values
    ------------
    Parameters:
        data: Dataset to be processed
    ------------
    Returns:
        data: Original dataset with static parameters removed
    '''
    for col in data.columns:
        if len(pd.unique(data[col])) < 2:
            data.drop(col, axis=1, inplace=True)
    return data

def remove_first_column(data):
    data.drop(data.columns[0], axis=1, inplace=True)
    return data


def filter_feature(feature):
    # TODO add different filtering options as parameters, low priority
    '''
    Applies a butterworth signal filter to the target feature
    Originally used for filtering current data on drone

    ------------
    Parameters:
        feature: the data series to be filtered
    ------------
    Returns:
        filtered data series
    '''
    from scipy import signal
    c, d = signal.butter(8, 0.08, btype='lowpass')
    return signal.filtfilt(c, d, feature, padlen=0)




def generate_featureset(dataset, filename, time_column=1, trusted_variable=0,  bufferSize=400):
    '''
    Generates and saves the feature set and target parameter information to be used in learning model training
    and prediction
    The feature set is generated from the root-of-trust parameter over a rolling buffer window, tracking:
    {Ground Truth, Most recent crater, most recent peak, minimum crater in window, maximum peak in window
    average reading over window}
    For each window reading this feature set is updated and stored in a .csv log, along with the corresponding
    readings of each target parameter

    ------------
    Parameters:
        dataset: Preprocessed Pandas dataframe of dataset to be evaluated
        filename: output filename to be used for completed training data
        trusted_variable: name of the root-of-trust
        bufferSize: the number of readings to be considered each window.
                    # determines runtime performance and what behaviors are captured in feature set
                    # defaultvalue=400(based on drone data)

    ------------
    Outputs:
        filename.csv: Complete feature set and target training data based on root-of-trust
    '''
    print("Generating training data...")
    t_idx = trusted_variable
    trusted_variable = str(dataset.columns[trusted_variable])
    root_of_trust_unfiltered = dataset[trusted_variable]
    #print("unfiltered root of trust:", root_of_trust_unfiltered[:10])
    root_of_trust = filter_feature(root_of_trust_unfiltered)
    #dataset.drop(columns=[trusted_variable], axis=1, inplace=True)


    peaks = [[0, 0]]
    craters = [[0, 0]]
    peaksfull = [[0, 0]]
    cratersfull = [[0, 0]]
    maxPeak = [0,0]
    minCrater = [0,0]
    total = 0
    rising = True

    # updated 11-17-22, still need to find a more universal solution for time column(all depends on dataset)
    if time_column != None:
        time = dataset.iloc[:, time_column]
        dataset.drop(dataset.columns[[time_column, t_idx]], axis=1, inplace=True)
    else:
        time = dataset.iloc[:, 0]
        if "Time" in dataset.columns:
            dataset.drop(columns=[trusted_variable], axis=1, inplace=True)
            dataset.drop(columns="Time", axis=1, inplace=True)
        if "ï»¿Time (s)" in dataset.columns:
            dataset.drop(columns=[trusted_variable], axis=1, inplace=True)
            dataset.drop(columns="ï»¿Time (s)", axis=1, inplace=True)

    filename += "_Training_Data.csv"
    outfile = open(filename, 'w')

    outfile.write("Time, " + trusted_variable + ", MR_Crater, MR_Peak, Min_Crater, Min_Crater_idx, Max_Peak, Max_Peak_idx, Rising, Average")
    for col in dataset.columns:
        if col != trusted_variable:
            outfile.write(", " + col)
    outfile.write('\n')

    buffer = pd.DataFrame({'time': [0] * bufferSize, 'ground_truth': [0] * bufferSize})
    window_length = time[bufferSize] - time[0]

    for i in range(1, len(dataset)):
        total -= buffer.iloc[0].ground_truth
        row = [time[i], root_of_trust[i]]
        
        buffer.loc[len(buffer)] = row        

        buffer = buffer.drop(buffer.index[0])
        buffer.reset_index(drop=True, inplace=True)

        total += buffer.iloc[-1].ground_truth
        avg = total / bufferSize


        # remove peaks/craters outside of time window
        if ((time[i] - float(peaks[0][0])) > 4):
            if len(peaks) > 1:
                del peaks[0]
                #maxPeak = max(peaks, key=lambda x: x[1])[1]
                maxPeak = peaks[peaks.index(max(peaks, key=lambda x: x[1]))]
        if ((time[i] - craters[0][0]) > 4):
            if len(craters) > 1:
                del craters[0]
                #minCrater = min(craters, key=lambda x: x[1])[1]
                minCrater = craters[craters.index(min(craters, key=lambda x: x[1]))]

        # detect peaks/craters
        if rising:
            if root_of_trust[i - 1] < root_of_trust[i]:
                rising = True
            elif abs(craters[len(craters) - 1][1] - root_of_trust[i - 1]) > 0.3:
                # print("peaks:", peaks)
                peaks.append([time[i - 1], root_of_trust[i - 1]])
                peaksfull.append([time[i - 1], root_of_trust[i - 1]])

                #maxPeak = max(peaks, key=lambda x: x[1])[1]
                maxPeak = peaks[peaks.index(max(peaks, key=lambda x: x[1]))]
                rising = False
        else:
            if root_of_trust[i - 1] > root_of_trust[i]:
                rising = False
            elif abs(peaks[len(peaks) - 1][1] - root_of_trust[i - 1]) > 0.3:
                # print("craters:", craters)
                craters.append([time[i - 1], root_of_trust[i - 1]])
                cratersfull.append([time[i - 1], root_of_trust[i - 1]])
                #minCrater = min(craters, key=lambda x: x[1])[1]
                minCrater = craters[craters.index(min(craters, key=lambda x: x[1]))]
                rising = True
        

        max_peak_time = (window_length - (time[i-1] - maxPeak[0]))/window_length
        min_crater_time = (window_length - (time[i-1] - minCrater[0]))/window_length
        # Add the feature set for this time period to training data
        line = str(time[i]) + ", " + str(root_of_trust[i]) + ", " + str(
            craters[-1][1]) + ", " + str(peaks[-1][1]) + ", " \
               + str(minCrater[1]) + ", " + str(min_crater_time) + ", " + str(maxPeak[1]) + ", " \
               + str(max_peak_time) + ", " + str(int(rising)) + ", " + str(avg)

        for col in dataset.columns:
            if col != trusted_variable:
                line += ", " + str(dataset[col].loc[i])
        line += '\n'

        outfile.write(line)

    outfile.close()
    print("Training data generated, saved to'", filename, "'")
