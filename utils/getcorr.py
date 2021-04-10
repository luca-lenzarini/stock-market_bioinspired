import pandas as pd
import numpy as np
import datetime as datetime


# TODO:
# COLOCAR COLUNA COMO PARAMETRO DA FUNÇÃO.


def getCorrelation(filepath, initialDate, finalDate, column_x, column_y):
    # load selected file path
    dataframe = pd.read_csv(filepath, index_col="Data",
                            dayfirst=True, parse_dates=[0])

    week = dataframe.loc[finalDate:initialDate]
    get_correlation = week[column_y].corr(
        week[column_x])
    print(get_correlation)

    return get_correlation
