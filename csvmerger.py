
import datacompy, pandas as pd
import numpy as np

def merge_csv(files_paths: list, merge_file_name="merged", index_keys=["Data"]):

    # if no index_key was passed
    if index_keys[0] == "Data":
        index_keys = ["Data"]*len(files_paths)

    # create empty dataframe
    fullDataframe = pd.DataFrame()

    for i in range(len(files_paths)):
        dataframe = pd.read_csv(files_paths[i], decimal=',')
        dataframe.rename(columns={index_keys[i]: 'Data'}, inplace = True)

        how = 'right'
        # check wich size has more rows
        if len(fullDataframe) > len(dataframe):
            how = 'left'

        if i != 0:
            # merge both dataframes
            fullDataframe = pd.merge(fullDataframe, dataframe, on='Data', how=how)
        else:
            # if it's the first dataframe, there is nothing to merge
            fullDataframe = dataframe

        # fill empty columns with previous or posterior values
        fullDataframe.fillna(method='ffill', inplace=True)
        fullDataframe.fillna(method='bfill', inplace=True)

    merge_file_name = merge_file_name + '.csv'

    print("Successfully merged into", merge_file_name)

    fullDataframe.to_csv(merge_file_name, index = False, header=True)

merge_csv(files_paths=['teste1.csv', 'teste2.csv'])