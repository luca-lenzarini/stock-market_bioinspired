from utils.utils import get_predictions
from utils.csvmerger import merge_csv
from utils.getcorr import *
from datetime import date, datetime

class Main:
    def __init__(self, files_path='./utils/SM_dataset/'):
        self.files_path = files_path
        self.suffix = ".csv"
        self.merged_file_separator = "_x_"

    def exec(self, main_stock, stocks_to_correlate, initialDate, finalDate, column):
        """"
            :param main_stock: 
            :param stocks_to_correlate:
            :param initialDate:
            :param finalDate:
            :param column: 
        """

        correlations = []

        # set the main stock file path
        main_file_path = self.getFullFilePath(main_stock)

        futureCorr = getFutureCorrelation(main_file_path, initialDate, finalDate, column)

        for i in range(len(stocks_to_correlate)):
            # defines current iteration stock file path
            file_path = self.getFullFilePath(stocks_to_correlate[i])

            # defines the name of the merged csv that will be created
            merged_file_name = self.merged_file_separator.join([main_stock, stocks_to_correlate[i]])

            # create new merge between the main stock market csv 
            merge_csv([main_file_path, file_path], merged_file_name)

            # get the correlation between them
            corr = getCorrelation(merged_file_name + self.suffix, initialDate,
                                finalDate, column+'_x', column+'_y')
            
            correlations.append(corr)
        

        print("correlations:", correlations)
        # run bio-inspired algorithms 
        get_predictions(correlations, futureCorr)


    def getFullFilePath(self, file_name):
        return self.files_path + file_name + self.suffix