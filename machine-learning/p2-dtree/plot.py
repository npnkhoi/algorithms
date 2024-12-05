import pandas as pd

decision_tree_df = pd.read_csv('cnf_output/DecisionTreeClassifier_report.csv')
bagging_df = pd.read_csv('cnf_output/BaggingClassifier_report.csv')
random_forest_df = pd.read_csv('cnf_output/RandomForestClassifier_report.csv')
gradient_boosting_df = pd.read_csv('cnf_output/GradientBoostingClassifier_report.csv')

import matplotlib.pyplot as plt
C_LIST = [300, 500, 1000, 1500, 1800]
D_LIST = [100, 1000, 5000]

for c in C_LIST:
    # plot the performances of the four models
    # y: accuracy
    # x: D
    plt.figure(dpi=200)
    plt.title(f'Accuracy vs dataset size for C = {c}')
    plt.xlabel('Dataset size')
    plt.ylabel('Accuracy')
    dfs_and_labels = [
        (decision_tree_df, 'DecisionTreeClassifier'),
        (bagging_df, 'BaggingClassifier'),
        (random_forest_df, 'RandomForestClassifier'),
        (gradient_boosting_df, 'GradientBoostingClassifier'),
    ]

    for df, label in dfs_and_labels:
        performances = [
            df[df['dataset'] == f'C={c}, D={d}']['acc'].values[0]
            for d in D_LIST
        ]
        plt.plot(D_LIST, performances, label=label, marker='o')
    
    plt.legend()
    plt.savefig(f'output/accuracy_vs_D_C_{c}.png')
    plt.close()
