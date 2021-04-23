import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta


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

def getFutureCorrelation(filepath, initialDate, finalDate, column):
    # load selected file path
    xDate = datetime.strptime(initialDate, "%m-%d-%Y").date()
    yDate = datetime.strptime(finalDate, "%m-%d-%Y").date()

    busday_init_final = np.busday_count(xDate, yDate).item()

    zDate = (yDate + timedelta(days=busday_init_final))

    busday_final_future = np.busday_count(yDate, zDate)

    days_to_add = (busday_init_final - busday_final_future).item()

    futureDate = (zDate + timedelta(days_to_add)).strftime("%m-%d-%Y")

    dataframe = pd.read_csv(filepath, index_col="Data",
                            dayfirst=True, parse_dates=[0], decimal=',')

    period = dataframe.loc[finalDate:initialDate]    
    future_period = dataframe.loc[futureDate:finalDate]
    
    
    final_correlation = period["Média Móvel E [200]"].corr(period["Média Móvel E [66]"])
    
    print("final_correlation ", final_correlation)
    return final_correlation