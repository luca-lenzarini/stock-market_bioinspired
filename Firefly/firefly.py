import random
import math
import numpy as np

def lplFirefly(n, gamma, alpha, beta, maxGeneration, probabilities, expected_value):

    """"
    :param n: number of fireflies in each generation
    :param gamma: absorption coefficient
    :param alpha: step of motion
    :param beta: attractivity factor
    :param maxGeneration: number of max generation
    :param probabilities: list of probabilities from events
    """
     
    d = len(probabilities)
    t = 0
    alphat = 1.0
    bests = [0]*d
    random.seed(0)  # Reset the random generator

    fireflies = []

    # Generating the initial locations of n fireflies
    for i in range(n):
        # Generate an array with d values
        weights = np.random.random(d)
        fireflies.append(weights)

    # Iterations or pseudo time marching

    r = []
    for i in range(n):
        lin = [0.0]*n
        r.append(lin)

    Z = [0]*n

    # Start iterations
    while t < maxGeneration: 
        for i in range(n):
            Z[i] = rmse(bayesian_evaluation(probabilities, fireflies[i], expected_value), expected_value)

        indice = np.argsort(Z)
        Z.sort()

        Z = [-x for x in Z]

        # Ranking the fireflies by their light intensity
        rank = [0]*n
        for i in range(n):
            rank[i] = fireflies[indice[i]]


        fireflies = rank

        for i in range(n):
            for j in range(n):
                r[i][j] = dist(fireflies[i], fireflies[j])

        alphat = alpha * alphat  # Reduce randomness as iterations proceed

        # Move all fireflies to the better locations
        for i in range(n):
            for j in range(n):
                if Z[i] < Z[j]:
                    threshold = np.random.random(d)

                    betat = beta*math.exp(-gamma*((r[i][j])**2))

                    if i != n-1:
                        for k in range(d):
                            fireflies[i][k] = ((1 - betat)*fireflies[i][k] + betat*fireflies[j][k] + alphat*threshold[k])/(1+alphat)

        bests = fireflies[0]

        t += 1

    print(bayesian_evaluation(probabilities, bests, expected_value))

    return bests

def bayesian_evaluation(probabilities, firefly, expected_value):

    prediction = 1

    # calculates the "inside part" of the formula
    for i in range(len(probabilities)):
        prediction *= ((1 - probabilities[i]) ** firefly[i])        

    prediction = 1 - prediction

    # return the Root-mean-square deviation
    return prediction

def dist(a, b):
    S = 0
    for k in range(len(a)):
        S += (a[k] - b[k]) ** 2
    S = math.sqrt(S)
    return S

def rmse(predictions, targets):    
    return math.sqrt(np.square(np.subtract(targets, predictions)).mean())