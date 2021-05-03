from utils.utils import get_predictions
from utils.csvmerger import merge_csv
from utils.correlation import *
from datetime import date, datetime

FILES_PATH = './utils/SM_dataset/'
SUFFIX = ".csv"
MERGED_FILE_SEPARATOR = "_x_"

def exec_train(main_stock, stocks_to_correlate, initialDate, finalDate, column):
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
    
    print("correlations:", correlations)
    # run bio-inspired algorithms 
    return get_predictions(correlations, futureCorr)

def exec_test(main_stock, stocks_to_correlate, initialDate, finalDate, column):

    # get the exponents for each stock 
    exponents = exec_train(main_stock, stocks_to_correlate, initialDate, finalDate, column)

    main_stock_filepath = './utils/SM_dataset/' + main_stock + SUFFIX

    # get the dataframe of the main stock
    main_stock_dataframe = pd.read_csv(main_stock_filepath, index_col="Data",
                            dayfirst=True, parse_dates=[0], decimal=',')

    # get the future dataframe
    future_dataframe = get_future_dataframe(main_stock_dataframe, initialDate, finalDate)

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

    for i in exponents.keys():
        print(i, eval.bayesian_evaluation(exponents[i]))

# helper method to fill full filepath name
def getFullFilePath(file_name):
    return FILES_PATH + getFilenameWithSuffix(file_name)

def getFilenameWithSuffix(file_name):
    return file_name + SUFFIX