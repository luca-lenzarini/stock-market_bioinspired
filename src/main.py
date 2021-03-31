from configparser import ConfigParser
import importlib as imp
import importlib.util
import os

config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'bio-algorithms', 'config.ini'))

algoritmos = config.sections()

for i in range(len(algoritmos)):
    algorithm = config[algoritmos[i]]

    if algorithm['active'] == 'true':
        # module = imp.import_module(algorithm['module'])

        print(os.path.join(os.path.dirname(__file__), 'bio-algorithms', algorithm['module'] + ".py"))

        spec = importlib.util.spec_from_file_location(algorithm['module'], os.path.join(os.path.dirname(__file__), 'bio-algorithms', algorithm['module'] + ".py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        function = eval('module.' + method_name + '(' + params_string + ')')

        print(algorithm['parameters'])

# def startAlgorithm(algorithm, params):
#     module_name = algs_modules[algorithm]['module']
#     method_name = algs_modules[algorithm]['method']

#     module = imp.import_module(module_name)    

#     params_string = ",".join(params)

#     function = eval('module.' + method_name + '(' + params_string + ')')

#     print(function)