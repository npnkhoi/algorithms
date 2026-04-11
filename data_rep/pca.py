import numpy as np
from utils import matrix_from_file

def pca(X: np.ndarray, k: int, centered: bool=False):
    mean = np.mean(X, 1)
    if centered:
        X = X - np.mean(X, 1, keepdims=True)
    print(mean)
    
    # assumes the rows are features
    cov = np.matmul(X, X.T) # mxm
    # print(cov)
    eig_vals, eig_vecs = np.linalg.eigh(cov)
    # print(eig_vals, eig_vecs)
    
    V = eig_vecs[:, -k:] # mxk
    A = np.matmul(V.T, X) # kxn
    # print(Xh)
    return V, A, mean

if __name__ == '__main__':
    X = matrix_from_file('mat1.txt')
    print(X)
    
    # # rank-1 approx
    # V, A = pca(X, 1)
    # Xh = V @ A
    # print(Xh)
    
    # # part 2: 2-PCA
    # V, A = pca(X, 2)
    
    # part 2: centered-PCA
    V, A, mean = pca(X, 2, True)
    print(A)