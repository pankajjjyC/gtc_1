# ARADISS abstraction v0.1
# Global Technology Connection, Inc.
# 6/29/2022
#
# Contains functions for ground truth and target parameter selection



def get_parameter_selection(columns):
    '''
    Function used to select which parameters should be considered in the dataset before generating ML feature sets
    Returns a boolean array to be used in dropping columns from pandas dataframe
    Currently implemented with basic console input, final version should have a UI front end using correlation graph
    ------------
    Parameters:
        columns: List of parameters to be selected from
    ------------
    Returns:
        selection: boolean array corresponding to parameters selected in column list
    '''
    num_cols = len(columns)
    print(columns)
    print("---Select which parameters to consider for training and testing---"
          "\nEnter x to finish selecting parameters.")
    # Boolean array to save selection makes dropping columns later easier
    selection = [True] * num_cols

    #s = input("Enter parameter:")
    s = "1" # drop time by default
    while s.isnumeric():
        if num_cols >= int(s) > 0:
            selection[int(s) - 1] = False
            s = input("Enter parameter:")
        else:
            break

    return selection


def auto_select_parameters(dataset, scores, threshold=0.5):
    from Aradiss.abstraction.correlations import dtw_correlations
    '''
    Automatically select which parameters should be dropped and which should be used for model training
    Currently uses the column average distance score as cutoff, can be changed later
    ------------
    Parameters:
        dataset: Preprocessed Pandas dataframe of dataset to be evaluated
        scores: Dataframe containing DTW distance scores for all parameter pairings
                # calculates new DTW scores if none given
        threshold: Cutoff limit of avg distance score to keep per parameters
    ------------
    Returns:
        selection: boolean array corresponding to parameters selected in column list
    '''

    if scores is None:
        scores = dtw_correlations(dataset)
    num_cols = len(dataset.columns)

    selection = [True] * num_cols
    #print("Scores:", scores)
    for i in range(len(dataset.columns)):
        if scores.iloc[:,i].mean() > threshold:
            selection[int(i)] = False
    print("Selection:", selection)
    return selection


def select_ground_truth(cols):
    '''
    Simple function used to select which column index will be used for the root-of-truth variable
    Intended for front end use
    ------------
    Parameters:
        cols: List of parameters to choose from
    ------------
    Returns:
        int index of root-of-trust
    '''
    print(cols)
    return int(input("Select ground truth:"))


def best_ground_truth(scores):
    '''
    Finds the ideal root-of-truth variable based on sum of normalized distance scores per column
    The parameter with the lowest cumulative distance score should have the strongest relations to other parameters
    # potentially add other qualifying features here later
    # Currently just selects lowest overall cumulative distance score as best ground truth candidate
    ------------
    Parameters:
        scores: Dataframe containing DTW distance scores for all parameter pairings
    ------------
    Returns:
        int index of root-of-trust
    '''
    scores['Sum'] = scores.sum(axis=1)
    scores['Sum'] = (scores['Sum'] - scores['Sum'].mean()) / scores['Sum'].std()
    best = scores['Sum'].idxmin()
    return scores.columns.tolist().index(best)


# need to clean this up and change it, just a rough working version for now
def select_parameters(dataset, ground_truth=0, params=''):
    '''
    Drops columns from dataframe, keeping only the selected parameters
    ------------
    Parameters:
        dataset: Pandas dataframe of dataset
        ground_truth: Index of root-of-trust parameter
        params: boolean array corresponding to indices to keep
    ------------
    Returns:
        dataset: Dataframe of dataset, now with only selected columns remaining

        # error for with params doesn't match columns
    '''
    # get name of ground truth column
    ground_truth_name = dataset.columns[ground_truth]
    cols = dataset.columns
    if(len( params)< 1):
        params = get_parameter_selection(dataset.columns)

    truth = dataset[ground_truth_name]
    print("Ground truth name:", ground_truth_name)
    dataset.drop(dataset.columns[[params]], axis=1, inplace=True)
    if ground_truth_name in dataset.columns:        
        dataset.drop(ground_truth_name, axis=1, inplace=True)
    dataset.insert(loc=0, column=ground_truth_name, value=truth)
    print(dataset)
    return dataset
