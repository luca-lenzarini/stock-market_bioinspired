from configparser import ConfigParser
import importlib as imp
import importlib.util
from datetime import *

from utils.evaluation import *

def get_exponents(probabilities: list, expected_value: float):

    config = ConfigParser()
    # read config file
    config.read('config.ini')

    # get all algorithms in the config file
    algoritmos = config.sections()

    # set the objective function of the problem
    function = Evaluation(probabilities, expected_value)
    obj_func = function.get_bayesian_rmse

    # set the dimension of the probabilities
    dim = len(probabilities)

    results_per_algoritm = {}

    # execute the algorithms 
    for i in range(len(algoritmos)):
        algorithm = config[algoritmos[i]]
        
        # verify the active algorithms 
        if algorithm['active'] == 'true':
            module = imp.import_module(algorithm['module'])
            result = eval('module.' + algorithm['function'] + '(' + algorithm['parameters'] + ')')

            results_per_algoritm[algorithm['name']] = result

    return results_per_algoritm

def get_exponent_with_params(probabilities, expected_value, parameters):
    
    config = ConfigParser()
    # read config file
    config.read('config.ini')

    # get all algorithms in the config file
    algoritmos = config.sections()

    # set the objective function of the problem
    function = Evaluation(probabilities, expected_value)
    obj_func = function.get_bayesian_rmse

    # set the dimension of the probabilities
    dim = len(probabilities)

    results_per_algoritm = {}

    # execute the algorithms 
    for i in range(len(algoritmos)):
        algorithm = config[algoritmos[i]]
        
        # verify the active algorithms 
        if algorithm['active'] == 'true':         
           
            module = imp.import_module(algorithm['module'])
            result = eval('module.' + algorithm['function'] + '(dim, ' + str(parameters.get(algorithm['function']))[1:-1] + ', obj_func)')

            results_per_algoritm[algorithm['name']] = result

    return results_per_algoritm

def get_future_dataframe(dataframe, initialDate, finalDate):
    
    # filters the period
    period = dataframe.loc[finalDate:initialDate] 

    # gets the size of the filtered period
    num_rows = len(period)

    i = 0
    # search for the last element of filtered period 
    for row in dataframe.itertuples():
        # if the indexes are the same, stop the iteration
        if(row[0] == period.index[0]):
            break

        i += 1

    # start row is the next row after period
    start_row = i - 1
    end_row = start_row - num_rows

    # filters the future period by the indexes
    return dataframe.iloc[end_row:start_row, :]

def get_future_date_period(initialDate, finalDate):
    initialDatetime = datetime.strptime(initialDate, '%m-%d-%Y')
    finalDatetime = datetime.strptime(finalDate, '%m-%d-%Y')

    days_to_add = finalDatetime - initialDatetime

    new_initialDate = (finalDatetime + timedelta(1)).strftime('%m-%d-%Y')
    new_finalDate = (finalDatetime + timedelta(1) + days_to_add).strftime('%m-%d-%Y')

    return {
        "initialDate": new_initialDate,
        "finalDate": new_finalDate
    }