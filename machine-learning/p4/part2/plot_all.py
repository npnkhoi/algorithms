from train import DATASETS
import numpy as np
import json

NROWS, NCOLS = 2, 5

algos = [
    ("single", "../data/clt_results.json"),
    ("mixture_em", "../data/mixture10_results.json"),
    ("forest", "../data/forest8_results.json")
]

raw_res = {
    model: json.load(open(result_path))
    for model, result_path in algos
}

# print(raw_res)

nice_res = {}
for model in raw_res:
    nice_res[model] = {}
    for dataset_name in raw_res[model]:
        results = raw_res[model][dataset_name]
        nice_res[model][dataset_name] = (np.mean(results), np.std(results))

# print(nice_res)

## Plot!

import matplotlib.pyplot as plt

fig, axs = plt.subplots(NROWS, NCOLS, figsize=(16, 6), sharex=True, dpi=150)
for it in range(10):
    irow = it // NCOLS
    icol = it % NCOLS
    dsname = DATASETS[it]

    xs = np.arange(3)
    ys = [nice_res[model][dsname][0] for model in nice_res]
    es = [nice_res[model][dsname][1] for model in nice_res]

    axs[irow, icol].errorbar(xs, ys, es, linewidth=1, fmt='o', ecolor='red', capsize=15)
    axs[irow, icol].set_title(dsname)

    if irow == NROWS-1:
        axs[irow, icol].set_xticks(xs, nice_res.keys())
    if icol == 0:
        axs[irow, icol].set_ylabel('log likelihood')

plt.tight_layout()

plt.savefig('out/plot-all.png')



