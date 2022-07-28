# ARADISS abstraction v0.1
# Global Technology Connection, Inc.
# 6/29/2022
#
# Contains functions for DTW score calculation
# Correlation graph generation


import numpy as np
import pandas as pd


def dtw_correlations(dataset, filename='', steps=0):
    from fastdtw import fastdtw
    from scipy.spatial.distance import euclidean
    '''
    Calculates the DTW distance between all parameters in a dataset and returns these scores as a correlation graph
    # Uses fastdtw() to calculate scores based on Euclidean distance using normalized data
    # Returned scores are min-max normalized, and returned as a 2d array, as well as saved to a .csv file
    ------------
    Parameters:
        dataset: Preprocessed Pandas dataframe of dataset to be evaluated
        filename: Filename prefix to be used for correlation graph .csv
        steps: How many elements to skip step-wise when calculating dtw score
                Default value = 1 + len(dataset)/10
                # Stepping necessary to reduces computational runtime
                # Still gives accurate estimation due to temporal flexibility of DTW
    ------------
    Returns:
        scores: DTW distance scores for all parameter-pairings stored as pandas dataframe
    ------------
    Outputs:
        filename_Correlation_Graph.csv: Distance score graph saved as .csv file
    '''
    if steps == 0:
        steps = 1 + int(len(dataset.iloc[:,0]) / 10)
        #print(len(dataset.iloc[:,0]))
        #print(steps)
    normalized_dataset = dataset.copy(deep = True)

    for col in dataset.columns:
        std = dataset[col].std()
        if std != 0:
            normalized_dataset[col] = (dataset[col] - dataset[col].mean()) / std

    normalized_dataset.replace(['NaN', 'NaT', 'inf', '-inf', np.inf, -np.inf], 0, inplace=True)

    num_cols = len(dataset.columns)
    scores = np.zeros(shape=(num_cols, num_cols))
    print("Calculating DTW distance scores...")
    for i in range(0, num_cols):
        print(dataset.columns[i])
        for j in range(i, num_cols):
            # Because DTW distance allows for some temporal discrepancy, taking only every nth element will still give
            # an appropriate distance score if the two datasets are somewhat correlated
            distance, path = fastdtw(normalized_dataset.iloc[::steps,i], normalized_dataset.iloc[::steps,j], dist=euclidean)
            scores[i, j] = distance
            scores[j, i] = distance
    scores = pd.DataFrame(scores, columns=dataset.columns, index=dataset.columns)
    scores = (scores-scores.min())/(scores.max()-scores.min())
    # filename2 = filename.split('.')
    # outfile = filename2[0] + "_Correlation_Graph.csv"
    # scores.to_csv(outfile, index=True)
    #print("Distance scores saved to", outfile)
    return scores


def draw_correlation_graph(scores):
    # TODO - placeholder, functionality to be determined based on front-end
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.heatmap(scores.iloc[:, :-1], xticklabels=True, yticklabels=True, square=True, cmap="YlGnBu")
    plt.show()
    # will use networkx to draw 2-layer graph reflecting correlation scores


def get_highest_correlations(scores):
    '''
    Finds the top 5 most correlated parameters for each parameter in the dataset
    ------------
    Parameters:
        scores: Dataframe containing DTW distance scores for all parameter pairings
    ------------
    Returns:
        dataframe with shape (n,5) listing the most correlated parameters and their scores for each parameter
    '''
    correlations = []
    cols = scores.columns

    for col in range(len(cols)):
        maxes = np.argpartition(scores.iloc[:, col], 5)     # use numpy.argpartition to do a partial sort in linear time
        maxes = maxes[:5]
        line = str(cols[col] + ": ")
        row = []
        for m in maxes:
            line += "{:>15}".format(str(cols[m])) + " = {:.3f} ".format(scores.iloc[m,col])
            row.append((int(m), scores.iloc[m,col]))
        correlations.append(row)

    return pd.DataFrame(correlations)