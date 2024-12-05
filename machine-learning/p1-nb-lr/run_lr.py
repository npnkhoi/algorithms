
import json

import numpy as np
from data import DATASETS, ENCODERS, vectorized_datsets
from models import LogisticRegression, NaiveBayes
import matplotlib.pyplot as plt
# import wandb
    

RESULT_FILE = 'res/lr.json'
SPLIT_RATIO = 0.7

if __name__ == "__main__":
    # wandb.init(
    #     entity='khoi-ml',
    #     project='cs6375',
    #     group='project1',
    # )
    results = {}
    for dataset_name in DATASETS:
        for encoder in ENCODERS:
            X_train, y_train, X_test, y_test = vectorized_datsets[f'{dataset_name}_{encoder}']

            # shuffle the train set and split into train/val
            indices = np.arange(len(y_train))
            np.random.seed(42)
            np.random.shuffle(indices)
            n_train = int(SPLIT_RATIO * len(indices))
            train_indices, val_indices = indices[:n_train], indices[n_train:]
            X_val, y_val = X_train[val_indices], y_train[val_indices]
            X_train, y_train = X_train[train_indices], y_train[train_indices]

            lambdas = [0.001, 0.01, 0.1]
            lrs = [0.001, 0.01, 0.1]

            best_val_acc = 0
            best_config = None
            for lamb in lambdas:
                for lr in lrs:
                    model = LogisticRegression(
                        lr=lr, n_iter=100, lamb=lamb, 
                        log_id=f'{dataset_name}_{encoder}',
                        patience=10
                    )
                    stop_iter, train_losses, val_losses, train_accs, val_accs = model.fit(X_train, y_train, X_val, y_val)

                    if val_accs[-1] > best_val_acc:
                        best_val_acc = val_accs[-1]
                        best_config = (lamb, lr)
                    
                    # print(f'{dataset_name} {encoder}, lambda={lamb}, lr={lr}\n\ttrain={train_accs[-1]:.5f}, val={val_accs[-1]:.5f}')
                    # plt.figure()
                    # plt.plot(train_accs, label='train')
                    # plt.plot(val_accs, label='val')
                    # plt.legend()
                    # plt.savefig(f'plots/{dataset_name}_{encoder}_lambda={lamb}_lr={lr}.png')
                    # print(f'plots/{dataset_name}_{encoder}_lambda={lamb}_lr={lr}.png')


            eval_res = model.evaluate(X_test, y_test)
            results[f'LR_{encoder}_{dataset_name}'] = eval_res

            print(f'{dataset_name} {encoder}')
            print(f'\tBest config: {best_config}')
            print(f'\tTest accuracy: {eval_res["accuracy"]:.5f}')

    json.dump(results, open(RESULT_FILE, 'w'), indent=4)