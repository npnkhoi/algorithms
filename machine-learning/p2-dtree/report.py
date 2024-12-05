from itertools import product
import json

import pandas as pd

ALGOS = [
    'RandomForestClassifier',
    'GradientBoostingClassifier',
    'BaggingClassifier',
    'DecisionTreeClassifier',
]
C_LIST = [300, 500, 1000, 1500, 1800]
D_LIST = [100, 1000, 5000]

for algo in ALGOS:
    df_data = []
    for c, d in product(C_LIST, D_LIST):
        report = json.load(open(f'cnf_output/{algo}_c{c}_d{d}/report.json'))
        best_params = report['best_params']
        if 'random_state' in best_params:
            del best_params['random_state']
        if 'n_jobs' in best_params:
            del best_params['n_jobs']
        
        df_data.append({
            'dataset': f'C={c}, D={d}',
            'acc': round(report['test_result']['acc'], 4),
            'f1': round(report['test_result']['f1'], 4),
            'best_params': best_params,
        })

    df = pd.DataFrame(df_data)
    df.to_csv(f'cnf_output/{algo}_report.csv', index=False)
