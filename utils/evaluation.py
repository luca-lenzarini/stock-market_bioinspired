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

    def bayesian_evaluation_percentage(self, exponents):
        result = self.bayesian_evaluation(exponents)

        if result > 0.5:
            return (result - 0.5) * 2
        elif result < 0.5: 
            return  (0.5 - result) * -2
        else: 
            return 0