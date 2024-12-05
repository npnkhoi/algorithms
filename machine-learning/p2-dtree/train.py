from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, GradientBoostingClassifier
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
C_LIST = [
    # 300, 500, 1000, 1500, 
    1800
]
D_LIST = [100, 1000, 5000]
MODEL_LIST = [
    DecisionTreeClassifier,
    # BaggingClassifier,
    # RandomForestClassifier,
    # GradientBoostingClassifier,
]

def train_and_test(model_class, param_dict, X_train, X_test, y_train, y_test):
    start_time = time.time()
    model = model_class(**param_dict)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    end_time = time.time()

    precision = np.mean(y_test[preds == 1] == 1)
    recall = np.mean(preds[y_test == 1] == 1)
    f1 = 2 * precision * recall / (precision + recall)
    acc = np.mean(preds == y_test)

    saved_param_dict = param_dict.copy()
    if model_class == BaggingClassifier:
        saved_param_dict['estimator'] = {
            'params': model.estimator_.get_params(),
        }
    
    return {
        'params': saved_param_dict,
        'num_nodes': model.tree_.node_count if model_class == DecisionTreeClassifier else None,
        'depth': model.tree_.max_depth if model_class == DecisionTreeClassifier else None,
        'acc': acc,
        'f1': f1,
        'recall': recall,
        'precision': precision,
        'seconds': end_time - start_time,
    }

def experiment(model_class, X_train, X_valid, X_test, y_train, y_valid, y_test, output_dir, args):
    if model_class == DecisionTreeClassifier:
        param_grid = {
            'random_state': [RANDOM_SEED],
            'criterion': ['gini', 'entropy'], # metrics for node impurity
            'splitter': ['best', 'random'], # 'random' means 'best random' -- wth?
            'max_depth': [None, 4, 16, 64], # None means based on min_samples_split
            'min_samples_split': [2, 8, 0.01, 0.1], # splits seems to make more sense than leaves...
            'max_features': ['sqrt', None], # number of features to consider when looking for the best split
        }
    elif model_class == BaggingClassifier:
        param_grid = {
            'random_state': [RANDOM_SEED],
            'n_jobs': [args.n_jobs],
            'estimator': [DecisionTreeClassifier(
                # best params from DecisionTreeClassifier experiment
                random_state=RANDOM_SEED, 
                criterion='gini',
                splitter='best',
                max_depth=None,
                min_samples_split=2,
                max_features=None,
            )],
            'n_estimators': [10, 50, 100],
            'max_samples': [0.1, 0.5, 1.0],
            'max_features': [0.1, 0.5, 1.0],
            'bootstrap': [True, False],
            'oob_score': [True, False],
            'warm_start': [True, False],
        }
    elif model_class == RandomForestClassifier:
        param_grid = {
            'random_state': [RANDOM_SEED],
            'n_jobs': [args.n_jobs],
            'criterion': ['gini'],
            'n_estimators': [10, 50, 100],
            'max_depth': [None, 4],
            'min_samples_split': [2, 0.01],
            'max_features': ['sqrt', None],
            'bootstrap': [True, False],
            'oob_score': [True, False],
        }
    elif model_class == GradientBoostingClassifier:
        param_grid = {
            'random_state': [RANDOM_SEED],
            'n_estimators': [10, 50, 100],
            'learning_rate': [0.1, 0.01],
            'criterion': ['friedman_mse', 'squared_error'],
            'max_depth': [3, None],
            'min_samples_split': [2, 0.01],
            'max_features': ['sqrt', None],
        }

    print('Training model...')

    best_acc = 0
    best_params = None
    saved_best_params = None
    report = {'grid_search': []}
    for params in product(*param_grid.values()):
        param_dict = dict(zip(param_grid.keys(), params))
        # Skip invalid combinations
        if model_class == BaggingClassifier:
            if param_dict['max_samples'] == 1.0 and param_dict['bootstrap'] == False:
                continue
            if not param_dict['bootstrap'] and param_dict['oob_score']:
                continue
            if param_dict['warm_start'] and param_dict['oob_score']:
                continue
        if model_class == RandomForestClassifier:
            if not param_dict['bootstrap'] and param_dict['oob_score']:
                continue

        
        result = train_and_test(model_class, param_dict, X_train, X_valid, y_train, y_valid)
        report['grid_search'].append(result)
        acc = result['acc']
        if acc > best_acc:
            best_acc = acc
            best_params = param_dict
            saved_best_params = result['params']


    print('Best params:', best_params)
    print('Best valid acc:', best_acc)
    report['best_params'] = saved_best_params

    X_train = np.concatenate([X_train, X_valid])
    y_train = np.concatenate([y_train, y_valid])

    result = train_and_test(model_class, best_params, X_train, X_test, y_train, y_test)

    report['test_result'] = result
    print('Test result:', report['test_result'])

    json.dump(report, open(f'{output_dir}/report.json', 'w'), indent=2)

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
    return X_train, X_test, y_train, y_test

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_jobs', type=int, default=4, help='Number of jobs to run in parallel.')
    parser.add_argument('--dataset', type=str, default='cnf', help='Dataset to use.', choices=['mnist', 'cnf'])
    args = parser.parse_args()

    if args.dataset == 'cnf':
        for model_class, C, D in tqdm(list(product(MODEL_LIST, C_LIST, D_LIST))):
            output_dir = f'cnf_output/{model_class.__name__}_c{C}_d{D}'
            os.makedirs(output_dir, exist_ok=True)
            print(f'Experimenting with {model_class.__name__} on C={C}, D={D}')
            print('Loading data...')
            train_df = pd.read_csv(f'all_data/train_c{C}_d{D}.csv', header=None)
            valid_df = pd.read_csv(f'all_data/valid_c{C}_d{D}.csv', header=None)
            test_df = pd.read_csv(f'all_data/test_c{C}_d{D}.csv', header=None)
            get_x_y = lambda df: (df.iloc[:, :-1].to_numpy(), df.iloc[:, -1].to_numpy())
            X_train, y_train = get_x_y(train_df)
            X_valid, y_valid = get_x_y(valid_df)
            X_test, y_test = get_x_y(test_df)
            # breakpoint()
            experiment(model_class, X_train, X_valid, X_test, y_train, y_valid, y_test, output_dir, args)
    else:
        X_train, X_test, y_train, y_test = download_mnist()
        y_train = y_train.astype(int).to_numpy()
        y_test = y_test.astype(int).to_numpy()
        X_train, X_test = X_train.to_numpy(), X_test.to_numpy()
        X_valid, y_valid = X_train[-10000:], y_train[-10000:]
        X_train, y_train = X_train[:-10000], y_train[:-10000]
        # breakpoint()
        for model_class in tqdm(MODEL_LIST):
            output_dir = f'mnist_output/{model_class.__name__}'
            os.makedirs(output_dir, exist_ok=True)
            print(f'Experimenting with {model_class.__name__} on MNIST')
            experiment(model_class, X_train, X_valid, X_test, y_train, y_valid, y_test, output_dir, args)


    
