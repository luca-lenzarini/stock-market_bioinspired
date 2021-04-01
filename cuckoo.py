# -*- coding: utf-8 -*-
"""
Created on Tue May 24 13:13:28 2016

@author: Hossam Faris
"""
import math
import numpy
import random
import time
from evaluation import get_bayesian_rmse
from evaluation import bayesian_evaluation
    
def get_cuckoos(nest,best,lb,ub,n,dim):
    
    # perform Levy flights
    tempnest=numpy.zeros((n,dim))
    tempnest=numpy.array(nest)
    beta=3/2;
    sigma=(math.gamma(1+beta)*math.sin(math.pi*beta/2)/(math.gamma((1+beta)/2)*beta*2**((beta-1)/2)))**(1/beta);

    s=numpy.zeros(dim)
    for j in range (0,n):
        s=nest[j,:]
        u=numpy.random.randn(len(s))*sigma
        v=numpy.random.randn(len(s))
        step=u/abs(v)**(1/beta)
 
        stepsize=0.01*(step*(s-best))

        s=s+stepsize*numpy.random.randn(len(s))
    
        tempnest[j,:]=numpy.clip(s, lb, ub)

    return tempnest

def get_best_nest(nest,newnest,fitness,n,dim,probabilities,expected_value):
# Evaluating all new solutions
    tempnest=numpy.zeros((n,dim))
    tempnest=numpy.copy(nest)

    for j in range(0,n):
    #for j=1:size(nest,1),
        fnew=get_bayesian_rmse(probabilities, newnest[j,:], expected_value)
        if fnew<=fitness[j]:
           fitness[j]=fnew
           tempnest[j,:]=newnest[j,:]
        
    # Find the current best

    fmin = min(fitness)
    K=numpy.argmin(fitness)
    bestlocal=tempnest[K,:]

    return fmin,bestlocal,tempnest,fitness

# Replace some nests by constructing new solutions/nests
def empty_nests(nest,pa,n,dim):

    # Discovered or not 
    tempnest=numpy.zeros((n,dim))

    K=numpy.random.uniform(0,1,(n,dim))>pa
    
    
    stepsize=random.random()*(nest[numpy.random.permutation(n),:]-nest[numpy.random.permutation(n),:])

    
    tempnest=nest+stepsize*K
 
    return tempnest
##########################################################################

def CS(lb,ub,n,N_IterTotal,probabilities,expected_value):
    
    """"
    :param lb: lower bound
    :param ub: uper bound
    :param n: number of cuckoos
    :param N_IterTotal: number of max iteration
    :param probabilities: list of probabilities 
    :param expected_value: expected result from probabilities
    """


    #lb=-1
    #ub=1
    #dim=3
    #n=50
    #N_IterTotal=1000
    
    dim = len(probabilities)
    
    # Discovery rate of alien eggs/solutions
    pa=0.25
    
    nd=dim

#    Lb=[lb]*nd
#    Ub=[ub]*nd
    convergence=[]

    # RInitialize nests randomely
    nest=numpy.random.rand(n,dim)*(ub-lb)+lb
       
    
    new_nest=numpy.zeros((n,dim))
    new_nest=numpy.copy(nest)
    
    bestnest=[0]*dim;
     
    fitness=numpy.zeros(n) 
    fitness.fill(float("inf"))
    

    # s=solution()

     
    # print("CS is optimizing  \""+objf.__name__+"\"")    
    
    timerStart=time.time() 
    # s.startTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    
    fmin,bestnest,nest,fitness =get_best_nest(nest,new_nest,fitness,n,dim,probabilities,expected_value)
    convergence = [];
    # Main loop counter
    for iter in range (0,N_IterTotal):
        # Generate new solutions (but keep the current best)
     
         timerStart2=time.time()
         new_nest=get_cuckoos(nest,bestnest,lb,ub,n,dim)
         
         
         # Evaluate new solutions and find best
         fnew,best,nest,fitness=get_best_nest(nest,new_nest,fitness,n,dim,probabilities,expected_value)
         
        
         new_nest=empty_nests(new_nest,pa,n,dim) ;
         
        
        # Evaluate new solutions and find best
         fnew,best,nest,fitness=get_best_nest(nest,new_nest,fitness,n,dim,probabilities,expected_value)
    
         if fnew<fmin:
            fmin=fnew
            bestnest=best
    
         #if (iter%1==0):
            #print(['At iteration '+ str(iter)+ ' the best fitness is '+ str(fmin)]);
         convergence.append(fmin)
         timerEnd2=time.time()
        #  s.iterationTime += timerEnd2 - timerStart2

    # timerEnd=time.time()  
    # s.endTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    # s.executionTime=timerEnd-timerStart
    # s.iterationTime = s.iterationTime/N_IterTotal
    # s.convergence=convergence
    # s.optimizer="CS"
    # # s.objfname=objf.__name__
    # s.bestIndividual=bestnest

    print(bayesian_evaluation(probabilities, bestnest, expected_value))

    return bestnest
    




 



