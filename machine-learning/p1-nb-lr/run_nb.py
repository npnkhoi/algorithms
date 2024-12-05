import json
from data import DATASETS, vectorized_datsets
from models import NaiveBayes
import os

def nb(data, encoder, algo, result_dict):
    assert encoder in ['bow', 'bernoulli']

    X_train, y_train, X_test, y_test = data
    model = NaiveBayes(algo)
    model.fit(X_train, y_train, n_classes=2)
    res = model.evaluate(X_test, y_test)
    print(f'{dataset_name} {encoder} {algo}: {res}')
    result_dict[f'{algo}_{encoder}_{dataset_name}'] = res
    

RESULT_FILE = 'res/nb.json'
SPLIT_RATIO = 0.7

if __name__ == "__main__":
    os.makedirs(os.path.dirname(RESULT_FILE), exist_ok=True)
    results = {}
    for dataset_name in DATASETS:
        nb(
            data=vectorized_datsets[f'{dataset_name}_bow'], 
            encoder='bow', 
            algo='multinomialNB',
            result_dict=results
        )

        nb(
            data=vectorized_datsets[f'{dataset_name}_bernoulli'],
            encoder='bernoulli',
            algo='discreteNB',
            result_dict=results
        )

    json.dump(results, open(RESULT_FILE, 'w'), indent=4)