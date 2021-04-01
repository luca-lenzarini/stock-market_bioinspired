from configparser import ConfigParser
import importlib as imp
import importlib.util
import os

def get_predictions(probabilities: list, expected_value: float):

    config = ConfigParser()
    config.read('config.ini')

    algoritmos = config.sections()

    for i in range(len(algoritmos)):
        algorithm = config[algoritmos[i]]

        probabilities_string = '[' + ', '.join([str(elem) for elem in probabilities]) + ']'

        if algorithm['active'] == 'true':
            print(algorithm['name'] + ':')
            module = imp.import_module(algorithm['module'])
            result = eval('module.' + algorithm['function'] + '(' + algorithm['parameters'] + ', ' + probabilities_string + ', ' + str(expected_value) + ')')

            print(result)
            print('\n')