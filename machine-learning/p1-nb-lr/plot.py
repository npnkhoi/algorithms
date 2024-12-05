import json
import matplotlib.pyplot as plt

results1 = json.load(open('res/nb.json', 'r'))
results2 = json.load(open('res/lr.json', 'r'))
results3 = json.load(open('res/sgd.json', 'r'))

results = {**results1, **results2, **results3}

DATASETS = ['enron1', 'enron2', 'enron4']
METRICS = ['accuracy', 'precision', 'recall', 'f1']
ALGOS = ['multinomialNB_bow', 'discreteNB_bernoulli', 'LR_bow', 'LR_bernoulli', 'SGD_bow', 'SGD_bernoulli']

fig, axs = plt.subplots(2, 2, figsize=(6, 6), dpi=300, sharey=True)  # Adjust figure size as needed

bar_width = 0.13
colors = plt.cm.get_cmap('tab10', len(ALGOS))  # Use the 'tab10' colormap for highly contrasting colors

for idx, metric in enumerate(METRICS):
    performances = []
    for dataset in DATASETS:
        row = []
        for algo in ALGOS:
            try:
                res = results[f'{algo}_{dataset}'][metric]
            except KeyError:
                res = 0
            row.append(res)
        performances.append(row)
    
    index = range(len(DATASETS))
    ax = axs[idx // 2, idx % 2]
    
    for i, algo in enumerate(ALGOS):
        algo_performance = [performances[j][i] for j in range(len(DATASETS))]
        ax.bar([p + bar_width * i for p in index], algo_performance, bar_width, label=algo, color=colors(i))
    
    if idx // 2 == 1:
        ax.set_xlabel('Datasets')
    if idx % 2 == 0:
        ax.set_ylabel('Performance')
    ax.set_title(f'{metric}')
    ax.set_xticks([p + bar_width * (len(ALGOS) / 2) for p in index])
    ax.set_xticklabels(DATASETS, rotation=45, ha='right')

# Create a single legend for all subplots
handles, labels = ax.get_legend_handles_labels()
LEGEND_ROOM = 0.1
fig.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.0))

plt.tight_layout(rect=[0, 0, 1, 1-LEGEND_ROOM])  # Adjust layout to make more room for the legend
plt.savefig('res/all_metrics.png')
plt.close()
