import sys
import os
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    prefix = sys.argv[1] # something like "compresss-koala"
    orig = sys.argv[2] # something like "Koala.png"
    orig_size = os.path.getsize(orig)
    KS = [2, 5, 10, 15, 20]

    plt.figure(dpi=150)
    res = {k: [] for k in KS}
    for k in KS:
        for samp in range(1, 6):
            file_path = f"{prefix}-{k}-{samp}.jpg"
            file_size = os.path.getsize(file_path)
            # print(k, samp, file_size)
            res[k].append(file_size/orig_size)
   
    ys = [np.mean(res[k]) for k in KS]
    es = [np.std(res[k]) for k in KS]
    plt.errorbar(KS, ys, es, capsize=10, fmt='--s', ecolor='r')
    plt.xlabel('num clusters')
    plt.ylabel('compression ratio')
    plt.title(orig)
    plt.tight_layout()
    plt.savefig(f'{prefix}-plot.png')


    
