from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier as KNN
import pandas as pd
import numpy as np
from itertools import product
import os
from tqdm import tqdm
import json
import time
import warnings
import argparse
import pickle
warnings.filterwarnings('ignore')

RANDOM_SEED = 42
MODEL_LIST = [
    SVC, 
    KNN
]

def train_and_test(model_class, param_dict, X_train, y_train, X_test, y_test):
    start_time = time.time()
    model = model_class(**param_dict)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    end_time = time.time()

    acc = np.mean(preds == y_test)

    saved_param_dict = param_dict.copy()
    
    return {
        'params': saved_param_dict,
        'acc': acc,
        'seconds': end_time - start_time,
    }

def try_model(model_class, X_train, y_train, X_test, y_test, output_dir, args):
    if model_class == SVC:
        param_grid = {
            'C': [0.1, 1, 10, 100],
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
        }
    elif model_class == KNN:
        param_grid = {
            'n_neighbors': [1, 3, 5, 7, 9, 11],
            'weights': ['uniform', 'distance'],
        }
    else:
        raise ValueError('Invalid model class')

    print('Training model...')

    ret = {
        'best': None,
        'grid_search': [],
    }
    best_acc = 0
    best_params = None
    param_sets = list(product(*param_grid.values()))
    for params in tqdm(param_sets, desc='Grid search'):
        param_dict = dict(zip(param_grid.keys(), params))
        result = train_and_test(model_class, param_dict, X_train, y_train, X_test, y_test)

        ret['grid_search'].append(result)

        if result['acc'] > best_acc:
            best_acc = result['acc']
            best_params = result['params']
    
    ret['best'] = {
        'params': best_params,
        'acc': best_acc,
    }

    print('Training complete')

    json.dump(ret, open(f'{output_dir}/report.json', 'w'), indent=2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_jobs', type=int, default=4, help='Number of jobs to run in parallel.')
    args = parser.parse_args()

    # Load data
    mnist_data = pickle.load(open('data/mnist.pkl', 'rb'))
    X_train, X_test, y_train, y_test = mnist_data['X_train'], mnist_data['X_test'], mnist_data['y_train'], mnist_data['y_test']
    y_train, y_test = y_train.astype(int).to_numpy(), y_test.astype(int).to_numpy()
    X_train, X_test = X_train.to_numpy(), X_test.to_numpy()
    
    for model_class in tqdm(MODEL_LIST):
        output_dir = f'out_mnist/{model_class.__name__}'
        os.makedirs(output_dir, exist_ok=True)
        print(f'Experimenting with {model_class.__name__} on MNIST')
        try_model(model_class, X_train, y_train, X_test, y_test, output_dir, args)


    
