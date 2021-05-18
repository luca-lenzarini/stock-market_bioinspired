from utils.utils import get_exponents
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

    results = []

    for i in range(len(exponents)):
        for j in exponents[i].keys():

            percentage = eval.bayesian_evaluation_percentage(exponents[i].get(j))

            results.append({ j: percentage })

    return results


def exec_mult_tests(main_stock, stocks_to_correlate, initialDate, finalDate, column, num_tests):

    results = []

    for i in range(num_tests):
        # print("==========================================")
        # print("TEST #{0}".format(i))
        results.append({"Test #" + str(i): exec_test(main_stock, stocks_to_correlate, initialDate, finalDate, column)})

    # for x in results:
    #     print (x)
    #     for y in results[x]:
    #         print (y,':',results[x][y])

    print(json.dumps(results, indent = 4))
    # print(results)
        

# helper method to fill full filepath name
def getFullFilePath(file_name):
    return FILES_PATH + getFilenameWithSuffix(file_name)

def getFilenameWithSuffix(file_name):
    return file_name + SUFFIX