# ARADISS abstraction v0.1.1
# Global Technology Connection, Inc.
# 7/29/2022
#
# Contains functions for DTW score calculation
# Correlation graph generation
# 7/29 - added converging version of dtw correlation function
#


import numpy as np
import pandas as pd


def dtw_correlations(dataset, filename='', steps=0, radius=1):
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
        steps = 1 + int(len(dataset.iloc[:,0]) / 1000)
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
            #print(j, end =", ")
            # Because DTW distance allows for some temporal discrepancy, taking only every nth element will still give
            # an appropriate distance score if the two datasets are somewhat correlated
            distance, path = fastdtw(normalized_dataset.iloc[::steps,i], normalized_dataset.iloc[::steps,j], dist=euclidean, radius=radius)
            scores[i, j] = distance
            scores[j, i] = distance
    maxVal = scores.max()
    scores = scores/maxVal
    scores = 1-scores
    scores = pd.DataFrame(scores, columns=dataset.columns, index=dataset.columns)

    filename = filename.split('.')
    outfile = filename[0] + "_Correlation_Graph_converged.csv"
    scores.to_csv(outfile, index=True)
    print("Distance scores saved to", outfile)
    return scores



def dtw_correlations_converge(dataset, filename='', window=0, min_iter=10, max_iter=120, start_idx=0, radius=1):
    from fastdtw import fastdtw
    from scipy.spatial.distance import euclidean
    from statistics import pstdev, mean
    '''
    # 11-17-22 update: changed to return inverted scores, so 0=uncorrelated, 1=correlated
    # Calculates the DTW distance between all parameters in a dataset and returns these scores as a correlation graph
    # Uses fastdtw() to calculate scores based on Euclidean distance using normalized data
    # This version calculates distance scores on a per-window basis, tracking the rolling average until convergence is achieved
    # Returned scores are min-max normalized, and returned as a 2d array, as well as saved to a .csv file
    ------------
    Parameters:
        dataset: Preprocessed Pandas dataframe of dataset to be evaluated
        filename: Filename prefix to be used for correlation graph .csv
        window: number of indices considered per window
        min_iter: miniumum number of windows to be considered before convergence
        max_iter: maximum number of window steps allowed before moving to next parameter pairing
        start_idx: index within dataframe to begin sampling
    ------------
    Returns:
        scores: DTW distance scores for all parameter-pairings stored as pandas dataframe
    ------------
    Outputs:
        filename_Correlation_Graph_converged.csv: Distance score graph saved as .csv file
    '''
    if window == 0:
        window = 1 + int(len(dataset.iloc[:,0]) / 100)
    print("Window:", window)
    
    if min_iter < 1:
        min_iter=1
    if max_iter <= min_iter:
        max_iter = min_iter*2
        
        #####
    offset = int(start_idx / window)
    min_iter += offset
    max_iter += offset
    
    normalized_dataset = dataset.copy(deep = True)

    for col in dataset.columns:
        std = dataset[col].std()
        if std != 0:
            normalized_dataset[col] = (dataset[col] - dataset[col].mean()) / std

    normalized_dataset.replace(['NaN', 'NaT', 'inf', '-inf', np.inf, -np.inf], 0, inplace=True)

    num_cols = len(dataset.columns)
    scores = np.zeros(shape=(num_cols, num_cols))
    eps = np.finfo(float).eps
    print("Calculating DTW distance scores...")
    
    import matplotlib.pyplot as plt
    
    for i in range(0, num_cols):
        #scores[i,i] = 0
        print(dataset.columns[i])
        for j in range(i, num_cols):
            converged = False
            z=offset
            avg_sum = 0
            averages = []
            distances = []
            while z < max_iter and (z*window + window) < len(normalized_dataset.iloc[:,i]) and not converged:
                distance, path = fastdtw(normalized_dataset.iloc[z*window:(z*window + window),i],
                                         normalized_dataset.iloc[z*window:(z*window + window),j], dist=euclidean, radius=radius)
                avg_sum += distance
                distances.append(distance)
                averages.append(avg_sum/(len(averages)+1))                
                if z > min_iter and averages[-1] == 0:
                    converged = True
                if pstdev(averages[-min_iter:]) / (mean(averages[-min_iter:]+eps)) < 0.1 and z > min_iter:
                    converged = True
                z += 1
                
            scores[i, j] = averages[-1]
            scores[j, i] = averages[-1]
            '''
            print("ScoreIJ:", scores[i,j])
            print("ScoreJI:", scores[j,i])
            
            plt.plot(averages, label="Avg. Score")
            plt.plot(distances, label="Distance per window")
            #plt.xlim(0,80)
            plt.title(dataset.columns[i] + " - " + dataset.columns[j])
            plt.legend()
            plt.xlabel("Window")
            plt.ylabel("Distance Score")
            plt.show()
            
            print("stdfull", round(pstdev(averages),3), "\nstdmin:", round(pstdev(averages[-min_iter:]),3),
                  "\nMeanfull:", round((mean(averages+eps)),3), "\nMeanmin:", round((mean(averages[-min_iter:]+eps)),3))
            print("Converged score:", averages[-1])
            '''
    maxVal = scores.max()
    scores = scores/maxVal
    scores = 1-scores
    scores = pd.DataFrame(scores, columns=dataset.columns, index=dataset.columns)
    filename = filename.split('.')
    outfile = filename[0] + "_Correlation_Graph_converged.csv"
    scores.to_csv(outfile, index=True)
    print("Distance scores saved to", outfile)
    #scores = 1-scores.iloc[:, :]
    return scores

def pearson_correlations(dataset, filename='', min_periods=55):
    pearson_corrs = dataset.corr(method='pearson', min_periods=min_periods)
    corrs = pearson_corrs.iloc[:, :]
    corrs = abs(corrs)
    filename = filename.split('.')
    outfile = filename[0] + "_Pearson_scores.csv"
    corrs.to_csv(outfile, index=True)
    print("Pearson correlation scores saved to", outfile)
    return(corrs)

def draw_correlation_graph(scores, size=10):
    # TODO - placeholder, functionality to be determined based on front-end
    import seaborn as sns
    import matplotlib.pyplot as plt
    #sns.heatmap(scores.iloc[:, :-1], xticklabels=True, yticklabels=True, square=True, cmap="YlGnBu")
    plt.rcParams["figure.figsize"] = (size,size)
    sns.heatmap(scores.iloc[:, :], xticklabels=True, yticklabels=True, square=True, cmap="YlGnBu")
    plt.show()
    
def draw_correlation_barplot(scores, ground_truth_idx=0, fig_size=[7,5]):
    import matplotlib.pyplot as plt
    corrs = scores[scores.columns[ground_truth_idx]]

    plt.rcParams["figure.figsize"] = fig_size

    corrs = corrs.tolist()
    sorted_indices = np.argsort(corrs)

    plt.bar(np.arange(0,len(corrs)), [corrs[i] for i in sorted_indices[::-1]] )
    plt.xticks(ticks=np.arange(0, len(scores.columns)), labels=[scores.columns[i] for i in sorted_indices[::-1]], rotation=90)
    plt.title("Current Correlation Scores")
    plt.tight_layout()
    plt.show()


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