# ARADISS model.metrics v0.1
# Global Technology Connection, Inc.
# 7/2/2022
#
# Contains metric functions, including cusum error calculation

from tensorflow.keras import backend as K
import math
import numpy as np

import Aradiss.model.metrics


def recall_m(y_true, y_pred):
    '''
        From Keras 2.0
        'Only computes a batch-wise average of recall.'
        ------------
        Parameters:
            y_true: Series of true values
            y_pred: Series of model precitions
        ------------
        Outputs:
            recall: recall score
        '''
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    '''
        From Keras 2.0
        'Only computes a batch-wise average of precision. Computes the precision, a
        metric for multi-label classification of how many selected items are
        relevant.'
        ------------
        Parameters:
            y_true: Series of true values
            y_pred: Series of model precitions
        ------------
        Outputs:
            precision: precision score
        '''
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def f1_m(y_true, y_pred):
    '''
        From Keras 2.0
        'Only computes a batch-wise average of f1.'
        ------------
        Parameters:
            y_true: Series of true values
            y_pred: Series of model precitions
        ------------
        Outputs:
            f1: f1 score
        '''
    precision = Aradiss.model.metrics.precision_m(y_true, y_pred)
    recall = Aradiss.model.metrics.recall_m(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))


#  mean squared error
def MSE(y_true, y_pred):
    '''
        Mean squared error metric
        ------------
        Parameters:
            y_true: Series of true values
            y_pred: Series of model precitions
        ------------
        Outputs:
            mse: MSE score
    '''
    if len(y_true) != len(y_pred):
        return -1
    mse = 0.0
    for i in range(len(y_true)):
        mse += (y_true[i] - y_pred[i]) ** 2
    mse = mse / len(y_true)
    return mse


def RMSE(y_true, y_pred):
    '''
        Root mean squared error metric
        ------------
        Parameters:
            y_true: Series of true values
            y_pred: Series of model precitions
        ------------
        Outputs:
            rmse: RMSE score
    '''
    if len(y_true) != len(y_pred):
        return -1
    rmse = 0.0
    for i in range(len(y_true)):
        rmse += (y_true[i] - y_pred[i]) ** 2
    rmse = np.sqrt(rmse / len(y_true))
    return rmse


def RMSLE(y_true, y_pred):
    '''
        Root mean squared logarithmic error metric
        ------------
        Parameters:
            y_true: Series of true values
            y_pred: Series of model precitions
        ------------
        Outputs:
            rmsle: RMSLE score
    '''
    if len(y_true) != len(y_pred):
        return -1
    rmsle = 0.0
    for i in range(len(y_true)):
        rmsle += (math.log(y_true[i] + 1) - math.log(y_pred[i] + 1)) ** 2
    rmsle = np.sqrt(rmsle / len(y_true))
    return rmsle


# Mean absolute error
def MAE(y_true, y_pred):
    '''
        Mean absolute error metric
        ------------
        Parameters:
            y_true: Series of true values
            y_pred: Series of model precitions
        ------------
        Outputs:
            mae: MAE
    '''
    if len(y_true) != len(y_pred):
        return -1
    mae = 0.0
    for i in range(len(y_true)):
        mae += np.sqrt((y_true[i] - y_pred[i]) ** 2) / y_true[i]
    mae = mae / len(y_true)
    return mae


# Mean absolute percentage error
def MAPE(Y_actual, Y_Predicted):
    '''
        Mean absolute percentage error metric
        ------------
        Parameters:
            y_true: Series of true values
            y_pred: Series of model precitions
        ------------
        Outputs:
            mape: MAPE
    '''
    mape = 100 / len(Y_actual) * np.sum(2 * np.abs(Y_Predicted - Y_actual) / (np.abs(Y_actual) + np.abs(Y_Predicted)))
    return mape

# Added 11-20-22
# For all functions added today: need to add error checking, dimension checking, etc
def evaluate(y_true, y_pred, metric='MAPE'):
    # TODO - update from python 3.9 to 3.10+ and change this to a switch-case
    error_scores = np.zeros(len(y_true[0]),dtype=float)
    if metric == "MAPE":
        for parameter in range(len(y_true[0])):
            error_scores[parameter] = MAPE(y_true[:,parameter], y_pred[:,parameter])
        #
    elif metric == "MAE":
        for parameter in range(len(y_true[0])):
            error_scores[parameter] = MAE(y_true[:,parameter], y_pred[:,parameter])
    elif metric == "MSE":
        for parameter in range(len(y_true[0])):
            error_scores[parameter] = MSE(y_true[:,parameter], y_pred[:,parameter])
    elif metric == "RMSE":
        for parameter in range(len(y_true[0])):
            error_scores[parameter] = RMSE(y_true[:,parameter], y_pred[:,parameter])
    else:
        print("Invalid score metric given")
    return error_scores

# Added 11-20-22
def error_barplot(y_true, y_pred, metric='MAPE', parameter_names='', figsize=[9,4.5]):
    import matplotlib.pyplot as plt
    plt.rcParams['figure.figsize'] = figsize
    error_scores = evaluate(y_true, y_pred, metric=metric)
    idx = np.argsort(error_scores)
    ordered_names=parameter_names[idx[::-1]]
    scores = error_scores[idx[::-1]]
    plt.bar(idx, scores[idx], tick_label=ordered_names[idx])
    plt.xticks(rotation = 45)
    plt.ylabel(metric)
    plt.tight_layout()
    #plt.savefig('errorbar.png', dpi=250)
    plt.show()
    return

# Added 11-20-22
def plot_predictions(y_true, y_pred, parameter_names=None, error_scores=None, metric="MAPE", x_range=None, figsize=[9,3]):
    import matplotlib.pyplot as plt
    if x_range is None:
        x_range = [0, len(y_true[:,0])]
    if error_scores is None:
        error_scores = evaluate(y_test, y_pred, metric=metric) 
    if parameter_names is not None:
        for parameter in range(len(parameter_names)):
            plt.rcParams['figure.figsize'] = figsize
            plt.plot(y_true[:,parameter], linewidth=2, label='True', alpha=0.8)
            plt.plot(y_pred[:,parameter], linewidth=2, label='Prediction', alpha=0.8)
            plt.legend()
            title = str(parameter_names[parameter])
            plt.title(title + "," + metric + ":" + str(round(error_scores[parameter],4)))
            plt.xlabel("Reading")
            plt.ylabel(title)
            plt.xlim(x_range)
            plt.tight_layout()
            plt.show()

    else:
        for parameter in range(len(y_true[0])):
            plt.rcParams['figure.figsize'] = figsize
            plt.plot(y_true[:,parameter], linewidth=2, label='True', alpha=0.8)
            plt.plot(y_pred[:,parameter], linewidth=2, label='Prediction', alpha=0.8)
            plt.legend()            
            title = str(parameter)
            plt.title("Column -" + title + "," + metric + ":" + str(round(error_scores[parameter],4)))
            plt.xlabel("Reading")
            plt.ylabel(title)
            plt.xlim(range)
            plt.tight_layout()
            plt.show()
    
    
# Cumulative error function for CUSUM
def cusum_error(Y_actual, Y_Predicted, windowSize, weight):
    '''
        Error calculation used for CUSUM detection method
        Takes the root of the squared absolute error, divided by the previous reading, summed across the entire window
        The most recent reading is given a different weight, to factor for more than 1/w worth of the error score
        e = (b*w) * sqrt(abs(Yt-Yp)**2) / Yt[-1]
        ------------
        Parameters:
            Y_actual: Series of true values
            Y_Predicted: Series of model precitions
            windowSize: the number of readings being considered in the error sum
            weight: how heavily the most recent reading is weighed in the sum
        ------------
        Outputs:
            e: cusum error, scaled down by 1000x
    '''
    e = 0
    if (Y_actual.size < windowSize or Y_Predicted.size < windowSize or Y_actual.size != Y_Predicted.size):
        return math.sqrt((Y_Predicted - Y_actual) ** 2) * 0.0001

    e = (windowSize * weight) * abs(math.sqrt((Y_actual[Y_actual.size - 1] - Y_Predicted[Y_Predicted.size - 1]) ** 2)) / abs(Y_actual[
            Y_actual.size - 1])
    for i in range(1, windowSize):
        e += abs(((math.sqrt((Y_actual[Y_actual.size - i] - Y_Predicted[Y_Predicted.size - i]) ** 2)) / abs(Y_actual[
            Y_actual.size - i])))
    return e * 0.0001


def cusum_stddev(Summed_error, average):
    # TODO check if average is used for calls from any script. Depreciated, remove
    '''
        finds the standard deviation over a CUSUM window
        Used for anomaly detection threshold
        ------------
        Parameters:
            Summed_error: Series of cusum error calculations
        ------------
        Outputs:
            stddev: standard deviation
    '''
    sum = 0
    for i in range(len(Summed_error) - 1):
        sum += ((Summed_error[i + 1] - Summed_error[i]) ** 2)
    sum /= len(Summed_error)
    return math.sqrt(sum)