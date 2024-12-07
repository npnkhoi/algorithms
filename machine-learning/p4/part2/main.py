from CLT_class import CLT
from Util import Util
from MIXTURE_CLT import MIXTURE_CLT
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    'model_type', type=str, choices=['clt', 'mixture'], 
    help='Type of model to use: clt or mixture'
)
parser.add_argument(
    '--n_components', '-n', type=int, default=2, 
    help='Number of components for the mixture model'
)
args = parser.parse_args()

n_sample = 5 if args.model_type == 'mixture' else 1

DATA_PATH = "../data/project4/part2/dataset/dataset"
DATASETS = [
    'accidents', 
    # 'baudio', 'bnetflix', 'jester', 'kdd', 'msnbc', 'nltcs', 'plants', 'pumsb_star', 'tretail'
]

results = {}

for dataset_name in DATASETS:
    print(f"Dataset: {dataset_name}")
    trainset = Util.load_dataset(f"{DATA_PATH}/{dataset_name}.ts.data")
    testset = Util.load_dataset(f"{DATA_PATH}/{dataset_name}.test.data")
    results[dataset_name] = []
    
    for i in range(n_sample):
        if args.model_type == 'clt':
            model = CLT()
        elif args.model_type == 'mixture':
            model = MIXTURE_CLT(n_components=args.n_components)
        
        # train
        model.learn(trainset)

        # test
        ll = model.computeLL(testset) / testset.shape[0]
        results[dataset_name].append(ll)
        
        print(f"sample {i}: {ll}")

with open(f'../data/{args.model_type}_results.json', 'w') as f:
    json.dump(results, f, indent=4)