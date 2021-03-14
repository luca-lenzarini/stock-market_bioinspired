from configparser import ConfigParser
import importlib as imp

algs_modules = ConfigParser()
algs_modules.read('algs_modules.ini')

def startAlgorithm(algorithm, params):
    module_name = algs_modules[algorithm]['module']
    method_name = algs_modules[algorithm]['method']

    module = imp.import_module(module_name)    

    params_string = ",".join(params)

    function = eval('module.' + method_name + '(' + params_string + ')')

    print(function)