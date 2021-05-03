import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from utils.utils import *


def getCorrelation(filepath, initialDate, finalDate, column_x, column_y):
    # load selected file path
    dataframe = pd.read_csv(filepath, index_col="Data",
                            dayfirst=True, parse_dates=[0])

    week = dataframe.loc[finalDate:initialDate]
    correlation = week[column_y].corr(
        week[column_x])

    return correlation

def getFutureCorrelation(filepath, initialDate, finalDate, column):

    dataframe = pd.read_csv(filepath, index_col="Data",
                            dayfirst=True, parse_dates=[0], decimal=',')

    # filters the period
    period = dataframe.loc[finalDate:initialDate]

    future_period = get_future_dataframe(dataframe, initialDate, finalDate)
    
    # calculate the final correlation
    final_correlation = np.corrcoef(period[column], future_period[column])[0][1]
    
    print("Correlation between periods: ", final_correlation)
    return final_correlation