
from __future__ import print_function
import numpy as np
import sys
import time
from Util import *
from CLT_class import CLT

class MIXTURE_CLT():
    
    def __init__(self, n_components=2):
        self.n_components = n_components # number of components
        self.lambda_ = None # mixture probabilities
        self.clt_list =[]   # List of Tree Bayesian networks

    def random_init(self, dataset):
        N = dataset.shape[0]
        # Randomly initialize the chow-liu trees and the mixture probabilities
        # Your code for random initialization goes here
        self.clt_list = [CLT() for _ in range(self.n_components)]
        self.lambda_ = np.ones(self.n_components) / self.n_components

        for k in range(self.n_components):
            subset = np.random.choice(N, int(N/self.n_components), replace=False)
            self.clt_list[k].learn(dataset[subset])
        
        print(f"Initial lambda: {self.lambda_}")
        print(f"LL: {self.computeLL(dataset) / N}")
        

    '''
        Learn Mixtures of Trees using the EM algorithm.
    '''
    def learn(self, dataset, max_iter=50, epsilon=1e-5):
        N = dataset.shape[0]
        # For each component and each data point, we have a weight
        gamma = np.zeros((self.n_components,dataset.shape[0]))

        # Randomly initialize the chow-liu trees and the mixture probabilities
        self.random_init(dataset)

        lls = []

        for itr in range(max_iter):
            # E-step: Complete the dataset to yield a weighted dataset
            # We store the weights in an array weights[ncomponents,number of points]
            
            for k in range(self.n_components):
                for i in range(N):
                    gamma[k,i] = self.lambda_[k] * self.clt_list[k].getProb(dataset[k])
            
            # Normalize the weights
            gamma = gamma / np.sum(gamma, axis=0) # TODO: check axis

            P = gamma.copy()
            Gamma = np.sum(gamma, axis=1)
            P = gamma / Gamma[:, np.newaxis]
            
            
            # M-step: Update the Chow-Liu Trees and the mixture probabilities
            for k in range(self.n_components):
                # Update the mixture probabilities
                self.lambda_[k] = Gamma[k] / N
                
                # Update the chow-liu tree for the kth component
                self.clt_list[k].update(dataset, P[k])
            
            # Compute the log-likelihood of the dataset
            ll = self.computeLL(dataset) / N
            lls.append(ll)
            
            print(f"Iteration {itr}: ll={ll}, lambdas={self.lambda_}")
            if itr > 0 and np.abs(lls[itr] - lls[itr - 1]) < epsilon:
                print(f"Converged after {itr} iterations")
                break
            # breakpoint()
                
    
    """
        Compute the log-likelihood score of the dataset
    """
    def computeLL(self, dataset):
        ll = 0.0
        # Write your code below to compute likelihood of data
        #   Hint:   Likelihood of a data point "x" is sum_{c} P(c) T(x|c)
        #           where P(c) is mixture_prob of cth component and T(x|c) is the probability w.r.t. chow-liu tree at c
        #           To compute T(x|c) you can use the function given in class CLT
        for i in range(dataset.shape[0]):
            sample_likelihood = 0.0
            for j in range(self.n_components):
                sample_likelihood += self.lambda_[j] * self.clt_list[j].getProb(dataset[i])
            ll += np.log(sample_likelihood)
        return ll
    

    
'''
    After you implement the functions learn and computeLL, you can learn a mixture of trees using
    To learn Chow-Liu trees, you can use
    mix_clt=MIXTURE_CLT()
    ncomponents=10 #number of components
    max_iter=50 #max number of iterations for EM
    epsilon=1e-1 #converge if the difference in the log-likelihods between two iterations is smaller 1e-1
    dataset=Util.load_dataset(path-of-the-file)
    mix_clt.learn(dataset,ncomponents,max_iter,epsilon)
    
    To compute average log likelihood of a dataset w.r.t. the mixture, you can use
    mix_clt.computeLL(dataset)/dataset.shape[0]
'''

    
    


    