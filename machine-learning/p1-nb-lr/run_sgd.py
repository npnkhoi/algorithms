import json
from data import DATASETS, ENCODERS, vectorized_datsets
from sklearn.linear_model import SGDClassifier
import os

from models import MySGD

RESULT_FILE = 'res/sgd.json'
SPLIT_RATIO = 0.7

if __name__ == "__main__":
    results = {}
    
    params = json.load(open('params_sgd.json', 'r'))
    for dataset_name in DATASETS:
        for encoder in ENCODERS:
            X_train, y_train, X_test, y_test = vectorized_datsets[f'{dataset_name}_{encoder}']

            param_here = params[f'SGD_{encoder}_{dataset_name}']['best_params']
            sgd = SGDClassifier(max_iter=1000, tol=1e-3, random_state=42, **param_here)
            model = MySGD(sgd)
            model.fit(X_train, y_train)
            result = model.evaluate(X_test, y_test)
            
            results[f'SGD_{encoder}_{dataset_name}'] = result

            print(f'{dataset_name} {encoder}')
            print(f'\tBest config: {param_here}')
            print(f'\t Accuracy: {result["accuracy"]:.5f}, Precision: {result["precision"]:.5f}, Recall: {result["recall"]:.5f}, F1: {result["f1"]:.5f}')

    json.dump(results, open(RESULT_FILE, 'w'), indent=4)
