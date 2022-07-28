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
    filename = filename.split('.')
    outfile = filename[0] + "_Correlation_Graph.csv"
    scores.to_csv(outfile, index=True)
    print("Distance scores saved to", outfile)
    return scores