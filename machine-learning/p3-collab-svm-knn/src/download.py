"""
Download MNIST
"""

import pickle

def download_mnist():
    from sklearn.datasets import fetch_openml
    # Load data from https://www.openml.org/d/554
    print('Downloading')
    X, y = fetch_openml('mnist_784', version=1, return_X_y=True)
    print('Downloaded')
    X = X / 255.
    # rescale the data, use the traditional train/test split
    # (60K: Train) and (10K: Test)
    X_train, X_test = X[:60000], X[60000:]
    y_train, y_test = y[:60000], y[60000:]
    
    pickle.dump({
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
    }, open('data/mnist.pkl', 'wb'))

if __name__ == '__main__':
    download_mnist()