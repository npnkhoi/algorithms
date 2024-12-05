"""
Implementation of collaborative filtering

num movies: M = 2e3
num users: U = 3e4
num training edges: E = 3e6 (max num edges: MU = 6e7)
num test edges: 1e5
"""

import pickle
import time
from typing import Dict, Tuple
import numpy as np
from tqdm import tqdm

def train() -> Tuple[np.ndarray, Dict, Dict]:
    print('reading training data')
    TRAINING_FILE = "data/netflix/TrainingRatings.txt"
    with open(TRAINING_FILE) as f:
        lines = f.readlines()
        training_set = [line.strip().split(',') for line in lines if line.strip()]

    user2uid = {}
    movie2mid = {}

    # compress the ids
    for line in training_set:
        movie = int(line[0])
        user = int(line[1])
        
        # map user and movie to unique ids
        if user not in user2uid:
            user2uid[user] = len(user2uid)
        if movie not in movie2mid:
            movie2mid[movie] = len(movie2mid)
    
    u = len(user2uid)
    m = len(movie2mid)
    
    # create the matrix X of [u, m] -> rating
    print('creating the matrix V')
    V = np.full((u, m), 0) # rating matrix
    M = np.zeros((u, m)) # mask matrix
    for line in training_set:
        movie = int(line[0])
        user = int(line[1])
        rating = float(line[2])
        V[user2uid[user], movie2mid[movie]] = rating
        M[user2uid[user], movie2mid[movie]] = 1
    
    # compute the mean rating for each user
    B = np.zeros(u)
    for uid in range(u):
        B[uid] = np.mean(V[uid, M[uid] == 1])

    # center the matrix X
    X = V - B[:, np.newaxis]
    X = X * M # zero out the missing values
    
    # compute the similarity matrix W
    print('computing the similarity matrix W')
    S = np.sqrt(np.multiply(X, X).sum(axis=1, keepdims=True))
    print((S==0).sum())
    denom = S @ S.T
    denom[denom == 0] = 1
    W = X @ X.T / denom
    W -= np.diag(np.diag(W)) # zero out the diagonal

    # reconstruct the full matrix X
    # X = W @ X / W.sum(axis=1, keepdims=True) + B[:, np.newaxis]

    return X, W, B, user2uid, movie2mid
    
def eval(X, W, B, user2uid, movie2mid) -> Dict:
    TEST_FILE = "data/netflix/TestingRatings.txt"
    with open(TEST_FILE) as f:
        lines = f.readlines()
        test_set = [line.strip().split(',') for line in lines if line.strip()]
    
    # compute the RMSE
    RMSE = 0
    MAE = 0
    for line in tqdm(test_set, desc="Evaluating"):
        movie = int(line[0])
        user = int(line[1])
        rating = float(line[2])
        u = user2uid[user]
        m = movie2mid[movie]

        # predict the rating
        mask = X[:, m] != 0 # only consider users who have rated the movie
        kappa = np.sum(np.abs(W[u, mask]))
        if kappa == 0:
            pred = B[u]
        else:
            pred = B[u] + W[u, mask] @ X[mask, m] / kappa
        
        RMSE += (pred - rating) ** 2
        MAE += np.abs(pred - rating)
    
    RMSE = np.sqrt(RMSE / len(test_set))
    MAE /= len(test_set)

    return {
        'RMSE': RMSE,
        'MAE': MAE
    }

def main():
    X, W, B, user2uid, movie2mid = train()
    res = eval(X, W, B, user2uid, movie2mid)
    print(res)

if __name__ == '__main__':
    tic = time.time()
    main()
    toc = time.time()   
    print('Elapsed time: {:.2f} seconds'.format(toc - tic))