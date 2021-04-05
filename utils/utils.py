from configparser import ConfigParser
import importlib as imp
import importlib.util

from utils.evaluation import *

def get_predictions(probabilities: list, expected_value: float):

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

    # execute the algorithms 
    for i in range(len(algoritmos)):
        algorithm = config[algoritmos[i]]
        
        # verify the active algorithms 
        if algorithm['active'] == 'true':
            print(algorithm['name'] + ':')

            module = imp.import_module(algorithm['module'])
            result = eval('module.' + algorithm['function'] + '(' + algorithm['parameters'] + ')')

            print(result)
            print('\n')