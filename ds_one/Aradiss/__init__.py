from Aradiss import abstraction
from Aradiss import anomalies
from Aradiss import model
from Aradiss.model import metrics
from Aradiss import detection


def find_raw_files(path='C:/Users/jpace.GLOBALTECH/PycharmProjects/ARADISS'):
    import glob
    import os
    os.chdir(path)
    raw_files = [os.path.basename(f) for f in glob.glob(path+"/*.csv") if "Training_Data" not in f]
    raw_files2 = [os.path.basename(f) for f in glob.glob(path+"/*.txt") if "Training_Data" not in f]
    #print(raw_files)
    for file in raw_files2:
        raw_files.append(file)
    return raw_files



def find_training_files(path='C:/Users/jpace.GLOBALTECH/PycharmProjects/ARADISS'):
    import glob
    import os
    os.chdir(path)
    training_files = [os.path.basename(f) for f in glob.glob(path+"/*Training_Data.csv")]
    return training_files
