from Util import Util
from CLT_class import CLT
import json

DATA_PATH = "../data/project4/part2/dataset/dataset"

DATASETS = ['accidents', 'baudio', 'bnetflix', 'jester', 'kdd', 'msnbc', 'nltcs', 'plants', 'pumsb_star', 'tretail']

results = {}
for dataset_name in DATASETS:
    dataset = Util.load_dataset(f"{DATA_PATH}/{dataset_name}.test.data")
    clt = CLT()
    clt.learn(dataset)
    ll = clt.computeLL(dataset) / dataset.shape[0]
    results[dataset_name] = ll
    print(f"{dataset_name}: {ll}")

with open('../data/p2_1_results.json', 'w') as f:
    json.dump(results, f, indent=4)