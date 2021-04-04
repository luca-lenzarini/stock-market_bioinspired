# -*- coding: utf-8 -*-
"""
Created on Thu May 26 02:00:55 2016

@author: hossam
"""
import math
import numpy
import random
import time
import copy

        
def BAT(d, N, Max_iteration, obj_func):
    
    n=N;      # Population size
    lb=0      # lower bound
    ub=1      # upper bound 
    N_gen=Max_iteration  # Number of generations

    A=0.5;      # Loudness  (constant or decreasing)
    r=0.5;      # Pulse rate (constant or decreasing)
    
    alpha = 0.95
    gamma = 0.05
    
    Qmin=0         # Frequency minimum
    Qmax=1         # Frequency maximum
    
    # Initializing arrays
    Q=numpy.zeros(n)  # Frequency
    v=numpy.zeros((n,d))  # Velocities
    
    # Initialize the population/solutions
    Sol=numpy.random.rand(n,d)
    #S=numpy.zeros((n,d))
    S=numpy.copy(Sol)
    Fitness=numpy.zeros(n)
    
    
    #Evaluate initial random solutions
    for i in range(0,n):
        Fitness[i] = obj_func(Sol[i,:])
    
    # Find the initial best solution
    fmin = min(Fitness)
    
    # Find the index of the initial best solution
    I=numpy.argmin(Fitness)

    # Sets the initial best solution 
    best = Sol[I,:]

    # Main loop
    for t in range (0,N_gen):
        # Loop over all bats(solutions)

        for i in range (0,n):
            Q[i]= Qmin + (Qmax-Qmin) * random.random()

            v[i,:]= v[i,:] + (Sol[i,:] - best) * Q[i]

            S[i,:]= Sol[i,:] + v[i,:]

            S[i,:]=numpy.clip(S[i,:], lb, ub)
        
            rnd = random.random()
            
            # Pulse rate
            if rnd > r:
                S[i,:] = best + 0.001 * numpy.random.randn(d)
                S[i,:] = numpy.clip(S[i,:], lb, ub)
        
            # Evaluate new solutions
            Fnew = obj_func(S[i,:])

            # Update if the solution improves
            if ((Fnew <= Fitness[i]) and (rnd < A) ):
                Sol[i,:] = S[i,:]
                Fitness[i] = Fnew            
        
            # Update the current best solution
            if Fnew <= fmin:
                best = copy.copy(S[i,:])
                fmin=Fnew
    
    return best
