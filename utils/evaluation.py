import math
import numpy as np

class Evaluation:
    def __init__(self, probabilities, expected_value):
        self.probabilities = probabilities
        self.expected_value = expected_value

    def get_bayesian_rmse(self, exponents):
        return self.rmse(self.bayesian_evaluation(exponents))

    def bayesian_evaluation(self, exponents):

        prediction = 0

        for i in range(len(self.probabilities)):
            calc = abs(self.probabilities[i]) ** exponents[i]

            if self.probabilities[i] < 0:
                prediction -= calc.real    
            else:
                prediction += calc.real

        return ((prediction / len(self.probabilities)) + 1 ) / 2

    def rmse(self, predictions):    
        return math.sqrt(np.square(np.subtract(self.expected_value, predictions)).mean())