
import datacompy, pandas as pd
import numpy as np

def merge_csv(files_names: list, index_keys: list, merge_file_name):

    fullDataframe = pd.DataFrame()

    for i in range(len(files_names)):
        dataframe = pd.read_csv(files_names[i], decimal=',')

        dataframe.rename(columns={index_keys[i]: 'Data'}, inplace = True)

        if i != 0:
            result = pd.merge(fullDataframe, dataframe, on='Data')
            fullDataframe = result
        else:
            fullDataframe = dataframe

    merge_file_name = merge_file_name + '.csv'

    print("Successfully merged into", merge_file_name)
    fullDataframe.to_csv(merge_file_name, index = False, header=True)