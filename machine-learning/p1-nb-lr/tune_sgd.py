import json
import numpy as np
from data import DATASETS, ENCODERS, vectorized_datsets
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os

RESULT_FILE = 'res_sgd.json'
SPLIT_RATIO = 0.7

if __name__ == "__main__":
    if os.path.exists(RESULT_FILE):
        results = json.load(open(RESULT_FILE, 'r'))
    else:
        results = {}
    for dataset_name in DATASETS:
        for encoder in ENCODERS:
            X_train, y_train, X_test, y_test = vectorized_datsets[f'{dataset_name}_{encoder}']

            # shuffle the train set and split into train/val
            X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=(1 - SPLIT_RATIO), random_state=42)

            param_grid = {
                'loss': ['hinge', 'log'],
                'penalty': ['l2', 'l1', 'elasticnet'],
                'alpha': [0.001, 0.01, 0.1],
                'learning_rate': ['constant', 'optimal', 'invscaling', 'adaptive'],
                'eta0': [0.001, 0.01, 0.1]
            }

            sgd = SGDClassifier(max_iter=1000, tol=1e-3, random_state=42)
            grid_search = GridSearchCV(sgd, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=3)
            grid_search.fit(X_train, y_train)

            best_model = grid_search.best_estimator_
            val_acc = accuracy_score(y_val, best_model.predict(X_val))

            predictions = best_model.predict(X_test)
            eval_res = {
                'accuracy': accuracy_score(y_test, predictions),
                'best_params': grid_search.best_params_,
                'val_accuracy': val_acc
            }
            results[f'SGD_{encoder}_{dataset_name}'] = eval_res

            print(f'{dataset_name} {encoder}')
            print(f'\tBest config: {grid_search.best_params_}')
            print(f'\tValidation accuracy: {val_acc:.5f}')
            print(f'\tTest accuracy: {eval_res["accuracy"]:.5f}')

    json.dump(results, open(RESULT_FILE, 'w'), indent=4)
