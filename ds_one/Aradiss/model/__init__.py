# ARADISS model v0.1
# Global Technology Connection, Inc.
# 7/2/2022
#
# init contains functions for default learning model functions and data handling

# functions here could be split into different modules, but it's more convenient to call things like
# model.tune_model or model.train rather than model.tune.tune_model

from Aradiss.model import *
import Aradiss.abstraction.data


def load_data(infile):
    '''
        Loads in pre-generated training/testing data, scales ground truth data, and returns dataframe of
        loaded dataset and and parameter names
        ------------
        Parameters:
            infile: filename of generated training data(including ground truth)
        ------------
        Outputs:
            trainingData: processed training data
            parameter_names: names of target columns
    '''
    from sklearn.preprocessing import MinMaxScaler
    trainingData = Aradiss.abstraction.data.load_dataset(infile)
    # TODO
    # consider adding another function call here to add new parameters via summation(i.e. motorRpm)

    # normalize ground truth feature set
    if 'Time' in trainingData.columns:
        trainingData.drop(columns='Time', inplace=True)
    #scaler = MinMaxScaler()
    #trainingData.iloc[:,:6] = scaler.fit_transform(trainingData.iloc[:,:6])
    parameter_names = trainingData.columns.values[9:]
    return trainingData, parameter_names


#split into training/testing
def train_split(train_data, test_data=None, test_percent=20, num_features=9):
    '''
        Splits training data into X and Y sets for training and testing, with X containing ground truth features
        ------------
        Parameters:
            train_data: Data the model will be trained on
            test_data: Dataset to test on(allows for different test/train sets)
            test_percent: Percentage of training data to use for testing
            num_features: Number of ground truth features contained in training data
        ------------
        Outputs:
            X: Ground truth features for training
            y: Target parameters for training
            X_test: Ground truth features for prediction
            y_test: Target parameters for prediction
    '''
    # TODO To make more modular, could add a flag in column name for ground truth features when generating training data
    # Then use this flag to determine which columns are X columns and which are Y
    # split must be consecutive, not randomized

    if test_data is not None:
        # TODO need to add exception blocks here
        X = train_data.iloc[:, :num_features].to_numpy()
        y = train_data.iloc[:, num_features:].to_numpy()
        X_test = test_data.iloc[:, :num_features].to_numpy()
        y_test = test_data.iloc[:, num_features:].to_numpy()
    else:
        test_start_index = int(len(train_data) - (len(train_data)*(0.01 * test_percent)))
        X_test = train_data.iloc[test_start_index:, :num_features].to_numpy()
        y_test = train_data.iloc[test_start_index:, num_features:].to_numpy()
        X = train_data.iloc[:test_start_index, :num_features].to_numpy()
        y = train_data.iloc[:test_start_index, num_features:].to_numpy()

    return X, y, X_test, y_test

# placeholder for ui, encapsulate in class later
def get_model_types():
    models = ["Gradient Boost Regressor"]
    return models

def select_model(selection='Gradient Boost Regressor'):
    '''
        Placeholder- will be used for selecting from different model types
        ------------
        Parameters:
            selection: Model type to be used

        ------------
        Outputs:
            model: Learning model
    '''
    # this is just a placeholder for now, until we decide how we want to select a model and
    # what models will be available
    # we can either use a string or an int for selection, depending on the ui is implemented
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.multioutput import MultiOutputRegressor
    if selection == 'Gradient Boost Regressor':
        model = MultiOutputRegressor(GradientBoostingRegressor())
    else:
        model = MultiOutputRegressor(GradientBoostingRegressor())
    return model

def train(model, X, y):
    '''
        Placeholder- will be implemented based on ui
        ------------
        Parameters:
            model: learning model
            X: Ground truth data
            y: Target parameters
        ------------
        Outputs:
            Trained model
    '''
    # placeholder
    # to be called from ui, allowing different datasets to train models
    model.fit(X, y)


def predict(model, x_true):
    '''
        Placeholder- will be implemented based on ui
        ------------
        Parameters:
            model: learning model
            x_true: Ground truth data
        ------------
        Outputs:
            pred: model prediction
    '''
    # placeholder
    # to be called from ui, allowing different options on what is predicted(length, dataset, etc)
    pred = model.predict(x_true)
    return pred

# placeholder, need to change/update after making model class
def save_prediction(y_pred, parameter_names, outfile=''):
    import pandas as pd
    y_df = pd.DataFrame(y_pred, columns=parameter_names)
    outfile += ".csv"
    y_df.to_csv(outfile, index=False)

