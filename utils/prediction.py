

def get_phi(probabilities, exponents):

    prediction = 0

    for i in range(len(self.probabilities)):
        calc = abs(self.probabilities[i]) ** exponents[i]

        if self.probabilities[i] < 0:
            prediction -= calc.real    
        else:
            prediction += calc.real

    return prediction / len(self.probabilities

def get_prediction(probabilities, exponents):
    return (get_phi(probabilities, exponents) + 1) / 2

def get_decision(probabilities, exponents):
    prediction = get_prediction(probabilities, exponents)

    if prediction > 0.5:
        return "buy"
    else if prediction < 0.5:
        return "sell"
    
    return "keep"