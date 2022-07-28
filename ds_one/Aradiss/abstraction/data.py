# ARADISS abstraction v0.1
# Global Technology Connection, Inc.
# 6/29/2022
#
# Contains functions for dataset loading, preprocessing
# DTW score calculation
# Correlation graph generation
# Ground truth and target parameter selection
# Creation of feature set and training data for learning models

import numpy as np
import pandas as pd


### This should be restructured into different modules, one for data loading/processing, and one for correlations
def load_dataset(infile):
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
    data = pd.read_csv(infile, encoding='latin-1')
    data = data.select_dtypes(exclude=['object'])

    data = drop_static_columns(data)
    # fill all invalid points
    data.replace(['NaN', 'NaT', 'inf', '-inf', np.inf, -np.inf], 0, inplace=True)
    data = data.fillna(0)
    data = data.reset_index(drop=True)
    # Other preprocessing considerations?
    return data


def drop_static_columns(data):
    '''
    Drops unchanging or static parameters from dataframe
    ------------
    Parameters:
        data: Dataset to be processed
    ------------
    Returns:
        data: Original dataset with static parameters removed
    '''
    for col in data.columns:
        std = data[col].std()
        if std == 0:
            data.drop(col, axis=1, inplace=True)
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


# We may possible need a function here to handle separately collected ground truth data, for example from microcontroller
# however this is on a case-by-case basis, so for now we will assume the ground truth is a column in the main csv


def generate_featureset(dataset, filename, trusted_variable=0,  bufferSize=400):
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
    trusted_variable = str(dataset.columns[trusted_variable])
    root_of_trust_unfiltered = dataset[trusted_variable]
    root_of_trust = filter_feature(root_of_trust_unfiltered)
    dataset.drop(columns=[trusted_variable], axis=1, inplace=True)

    peaks = [[0, 0]]
    craters = [[0, 0]]
    peaksfull = [[0, 0]]
    cratersfull = [[0, 0]]
    maxPeak = 0
    minCrater = 0
    total = 0
    rising = True

    # update this to find a more universal time solution
    time = dataset.iloc[:, 0]
    if "Time" in dataset.columns:
        dataset.drop(columns="Time", axis=1, inplace=True)

    outfile = open(filename, 'w')

    outfile.write("Time, " + trusted_variable + ", MR_Crater, MR_Peak, Min_Crater, Max_Peak, Average")
    for col in dataset.columns:
        if col != trusted_variable:
            outfile.write(", " + col)
    outfile.write('\n')

    buffer = pd.DataFrame({'time': [0] * bufferSize, 'ground_truth': [0] * bufferSize})

    for i in range(1, len(dataset)):
        if len(buffer) > len(buffer) - 2:
            total = total - buffer.iloc[0].ground_truth
            buffer = buffer.drop(buffer.index[0])
        buffer.loc[-1, 'time'] = time[i]
        buffer.loc[-1, 'ground_truth'] = root_of_trust[i]
        total = total + root_of_trust[i]
        avg = total / len(buffer['time'])

        # remove peaks/craters outside of time window
        if ((time[i] - float(peaks[0][0])) > 4):
            if len(peaks) > 1:
                del peaks[0]
                maxPeak = max(peaks, key=lambda x: x[1])[1]
        if ((time[i] - craters[0][0]) > 4):
            if len(craters) > 1:
                del craters[0]
                minCrater = min(craters, key=lambda x: x[1])[1]

        # detect peaks/craters
        if rising:
            if root_of_trust[i - 1] < root_of_trust[i]:
                rising = True
            elif abs(craters[len(craters) - 1][1] - root_of_trust[i - 1]) > 0.3:
                peaks.append([time[i - 1], root_of_trust[i - 1]])
                peaksfull.append([time[i - 1], root_of_trust[i - 1]])

                maxPeak = max(peaks, key=lambda x: x[1])[1]
                rising = False
        else:
            if root_of_trust[i - 1] > root_of_trust[i]:
                rising = False
            elif abs(peaks[len(peaks) - 1][1] - root_of_trust[i - 1]) > 0.3:
                craters.append([time[i - 1], root_of_trust[i - 1]])
                cratersfull.append([time[i - 1], root_of_trust[i - 1]])
                minCrater = min(craters, key=lambda x: x[1])[1]
                rising = True


        # Add the feature set for this time period to training data
        line = str(time[i]) + ", " + str(root_of_trust[i]) + ", " + str(
            craters[-1][1]) + ", " + str(peaks[-1][1]) + ", " \
               + str(minCrater) + ", " + str(maxPeak) + ", " + str(avg)

        for col in dataset.columns:
            if col != trusted_variable:
                line += ", " + str(dataset[col].loc[i])
        line += '\n'

        outfile.write(line)

    outfile.close()
