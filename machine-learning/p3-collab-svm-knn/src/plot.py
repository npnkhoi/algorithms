import json
import pandas as pd

import matplotlib.pyplot as plt

def plot_svc(ax):
    fn = 'out_mnist/SVC/report.json'
    data = json.load(open(fn))

    line_data = {}
    for report in data['grid_search']:
        params = report['params']
        acc = report['acc']
        sec = round(report['seconds'], 1)
        if params['kernel'] not in line_data:
            line_data[params['kernel']] = []
        line_data[params['kernel']].append((params['C'], acc, sec))
    for kernel, data in line_data.items():
        data.sort()
        x, y, s = zip(*data)
        ax.plot(x, y, label=kernel, marker='o')
    ax.legend()
    ax.set_xlabel('C')
    ax.set_ylabel('Accuracy')
    ax.set_xscale('log')
    ax.set_title('SVM Grid Search')

    # Export to CSV using pandas
    rows = []
    for kernel, data in line_data.items():
        for row in data:
            rows.append([kernel, *row])
    df = pd.DataFrame(rows, columns=['kernel', 'C', 'accuracy', 'seconds'])
    df.to_csv('out_mnist/SVC/results_svm.csv', index=False)

def plot_knn(ax):
    fn = 'out_mnist/KNeighborsClassifier/report.json'
    data = json.load(open(fn))

    line_data = {}
    for report in data['grid_search']:
        params = report['params']
        acc = report['acc']
        sec = round(report['seconds'], 1)
        if params['weights'] not in line_data:
            line_data[params['weights']] = []
        line_data[params['weights']].append((params['n_neighbors'], acc, sec))
    for weights, data in line_data.items():
        data.sort()
        x, y, s = zip(*data)
        ax.plot(x, y, label=weights, marker='o')
    ax.legend()
    ax.set_xlabel('n_neighbors')
    ax.set_ylabel('Accuracy')
    ax.set_title('KNN Grid Search')

    # Export to CSV using pandas
    rows = []
    for weights, data in line_data.items():
        for row in data:
            rows.append([weights, *row])
    df = pd.DataFrame(rows, columns=['weights', 'n_neighbors', 'accuracy', 'seconds'])
    df.to_csv('out_mnist/KNeighborsClassifier/results_knn.csv', index=False)

if __name__ == '__main__':
    fig, axs = plt.subplots(1, 2, figsize=(8, 6), dpi=300, sharey=True)
    plot_svc(axs[0])
    plot_knn(axs[1])
    plt.tight_layout()
    plt.savefig('out_mnist/combined_plot.png')