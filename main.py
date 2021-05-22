from utils.utils import get_exponents, get_exponent_with_params
from utils.csvmerger import merge_csv
from utils.correlation import *
from datetime import date, datetime
import json

FILES_PATH = './utils/SM_dataset/'
SUFFIX = ".csv"
MERGED_FILE_SEPARATOR = "_x_"

def exec_train(main_stock, stocks_to_correlate, initialDate, finalDate, column, n):
    """"
        :param main_stock: main stock to be correlate with others
        :param stocks_to_correlate: stocks to be correlated with main stock
        :param initialDate: initial filter date
        :param finalDate: final filter date
        :param column: column to be correlated
    """

    correlations = []

    # set the main stock file path
    main_file_path = getFullFilePath(main_stock)

    futureCorr = getFutureCorrelation(main_file_path, initialDate, finalDate, column)
    # futureCorr = 0.412412


    for i in range(len(stocks_to_correlate)):
        # defines current iteration stock file path
        file_path = getFullFilePath(stocks_to_correlate[i])

        # defines the name of the merged csv that will be created
        merged_file_name = MERGED_FILE_SEPARATOR.join([main_stock, stocks_to_correlate[i]])

        # create new merge between the main stock market csv 
        merge_csv([main_file_path, file_path], merged_file_name)

        # get the correlation between them
        corr = getCorrelation(merged_file_name + SUFFIX, initialDate,
                            finalDate, column+'_x', column+'_y')
        
        correlations.append(corr)

    exponents = []

    for i in range(n):
        # run bio-inspired algorithms 
        current_exponents = get_exponents(correlations, futureCorr)
        exponents.append(current_exponents)

    return exponents

def exec_train_parameters(main_stock, stocks_to_correlate, initialDate, finalDate, column, n):
    """"
        :param main_stock: main stock to be correlate with others
        :param stocks_to_correlate: stocks to be correlated with main stock
        :param initialDate: initial filter date
        :param finalDate: final filter date
        :param column: column to be correlated
    """

    correlations = []

    # set the main stock file path
    main_file_path = getFullFilePath(main_stock)

    futureCorr = getFutureCorrelation(main_file_path, initialDate, finalDate, column)

    for i in range(len(stocks_to_correlate)):
        # defines current iteration stock file path
        file_path = getFullFilePath(stocks_to_correlate[i])

        # defines the name of the merged csv that will be created
        merged_file_name = MERGED_FILE_SEPARATOR.join([main_stock, stocks_to_correlate[i]])

        # create new merge between the main stock market csv 
        merge_csv([main_file_path, file_path], merged_file_name)

        # get the correlation between them
        corr = getCorrelation(merged_file_name + SUFFIX, initialDate,
                            finalDate, column+'_x', column+'_y')
        
        correlations.append(corr)

    exponents = []

    firefly = {"params": [1, 0.8, 0.8, 0.5, 1], "steps": [1, 0.2, 0.2, 0.1, 1]} 
    cuckoo = {"params": [50,50], "steps": [10, 10]}
    bat = {"params": [1,50], "steps": [1, 10]}
    elephant = {"params": [50, 0.5, 0.5, 5, 50], "steps": [10, 0.1, 0.1, 5, 50]} 

    for i in range(n):
        algorithm_params = {"lplFirefly": firefly["params"], "CS": cuckoo["params"], "BAT": bat["params"], "elephant": elephant["params"]}

        # run bio-inspired algorithms 
        current_exponents = get_exponent_with_params(correlations, futureCorr, algorithm_params)
        exponents.append(current_exponents)

        for a in range(len(firefly["params"])):
            firefly["params"][a] += firefly["steps"][a]
            elephant["params"][a] += elephant["steps"][a]

        for a in range(len(cuckoo["params"])):
            cuckoo["params"][a] += cuckoo["steps"][a]
            bat["params"][a] += bat["steps"][a]

        # firefly["params"] = np.sum([firefly["params"], firefly["steps"]], axis=0)
        # cuckoo["params"] = np.sum([cuckoo["params"], cuckoo["steps"]], axis=0)
        # bat["params"] = np.sum([bat["params"], bat["steps"]], axis=0)
        # elephant["params"] = np.sum([elephant["params"], elephant["steps"]], axis=0)

    return exponents


def exec_test(main_stock, stocks_to_correlate, initialDate, finalDate, column, n):

    # get the exponents for each stock 
    exponents = exec_train(main_stock, stocks_to_correlate, initialDate, finalDate, column, n)

    future_period = get_future_date_period(initialDate, finalDate)

    future_correlations = []

    # get all dataframes from all stocks 
    for i in range(len(stocks_to_correlate)):
        # define file paths
        merged_stocks_filepath = getFilenameWithSuffix(main_stock + MERGED_FILE_SEPARATOR + stocks_to_correlate[i])

        # get correlation
        future_correlation = getCorrelation(merged_stocks_filepath, future_period["initialDate"], future_period["finalDate"], column + '_x', column + '_y')

        future_correlations.append(future_correlation)

    eval = Evaluation(future_correlations, 0)

    futureCorrelation = getFutureCorrelation(getFullFilePath(main_stock), initialDate, finalDate, column)

    final_result = 0

    if(futureCorrelation > 0.5):
        final_result = 1
    
    results = {"result": [final_result]*n}

    for i in range(len(exponents)):
        for j in exponents[i].keys():

            percentage = eval.bayesian_evaluation(exponents[i].get(j))

            if results.get(j) == None:
                results[j] = [percentage]
            else:
                results[j].append(percentage)

            # results.append({ j: percentage })

    return results

# helper method to fill full filepath name
def getFullFilePath(file_name):
    return FILES_PATH + getFilenameWithSuffix(file_name)

def getFilenameWithSuffix(file_name):
    return file_name + SUFFIX