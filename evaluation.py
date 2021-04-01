import math
import numpy as np

def get_bayesian_rmse(probabilities, exponents, expected_value):
    return rmse(bayesian_evaluation(probabilities, exponents, expected_value), expected_value)

def rmse(predictions, targets):    
    return math.sqrt(np.square(np.subtract(targets, predictions)).mean())

def bayesian_evaluation(probabilities, exponents, expected_value):

    prediction = 1

    # calculates the "inside part" of the formula
    for i in range(len(probabilities)):
        prediction *= ((1 - probabilities[i]) ** exponents[i])        

    prediction = 1 - prediction

    # return the Root-mean-square deviation
    return prediction