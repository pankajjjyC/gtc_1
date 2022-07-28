from Aradiss import abstraction
# from Aradiss import anomalies
# from Aradiss import model


def find_raw_files(path='C:/Users/jpace.GLOBALTECH/PycharmProjects/ARADISS'):
    import glob
    import os
    os.chdir(path)
    raw_files = [os.path.basename(f) for f in glob.glob(path+"/*[!Training_Data].csv")]
    return raw_files



def find_training_files(path='C:/Users/jpace.GLOBALTECH/PycharmProjects/ARADISS'):
    import glob
    import os
    os.chdir(path)
    training_files = [os.path.basename(f) for f in glob.glob(path+"/*Training_Data.csv")]
    return training_files
