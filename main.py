from utils.utils import get_predictions
from utils.csvmerger import merge_csv
from utils.getcorr import getCorrelation

# N CSV THEY WANT TO USE.
# DEFINE WICH STOCK HE WANTS TO PREDICT.
# DEFINE TIME
# GET CORRELATION


def exec(mainCSV, listCSV, initialDate, finalDate, column):
    """"
        :param mainCSV:
        :param listCSV:
        :param period:
    """

    correlations = []
    main_file_path = './utils/SM_dataset/' + mainCSV + '.csv'

    for i in range(len(listCSV)):
        file_path = './utils/SM_dataset/' + listCSV[i] + '.csv'
        merged_file_name = mainCSV + 'x' + listCSV[i]
        merge_csv([main_file_path, file_path], merged_file_name)
        corr = getCorrelation(merged_file_name + '.csv', initialDate,
                              finalDate, column+'_x', column+'_y')
        correlations.append(corr)

    get_predictions(correlations, 0.304058352)
