from CLT_class import CLT
from Util import Util
from MIXTURE_CLT import MIXTURE_CLT
from forest import CLTForest
import json
import argparse

DATA_PATH = "data/project4/part2/dataset/dataset"
DATASETS = [
    'accidents', 
    'baudio', 'bnetflix', 'jester', 'kdd', 'msnbc', 'nltcs', 'plants', 'pumsb_star', 'tretail'
]

def train(args: argparse.Namespace):
    """
    args contains everything needed
    """
    datasets = DATASETS[:1] if args.dataset == 'first' else DATASETS 
    results = {}

    for dataset_name in datasets:
        print(f"\nDataset: {dataset_name}")
        trainset = Util.load_dataset(f"{DATA_PATH}/{dataset_name}.ts.data")
        testset = Util.load_dataset(f"{DATA_PATH}/{dataset_name}.{args.eval_set}.data")
        results[dataset_name] = []
        
        for i in range(args.n_samples):
            print(f'\nSample {i}')

            # create model
            if args.model_type == 'clt':
                model = CLT()
            elif args.model_type == 'mixture':
                model = MIXTURE_CLT(n_components=args.n_components)
            elif args.model_type == "forest":
                n = trainset.shape[1]
                n_hidden = int(args.hidden_rate * (n**2))
                print(f"n_hidden = {n_hidden}")
                model = CLTForest(args.n_components, n_hidden)
            
            # train
            model.learn(trainset)

            # test
            ll = model.computeLL(testset) / testset.shape[0]
            results[dataset_name].append(ll)
            
            print(f"LL on Eval set: {ll}")

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'model_type', type=str, choices=['clt', 'mixture', 'forest'], 
        help='Type of model to use: clt, mixture, or forest'
    )
    parser.add_argument(
        '--n_components', '-n', type=int, default=2, 
        help='Number of components for the mixture model'
    )
    parser.add_argument(
        '--n_samples', '-s', type=int, default=5, 
        help='Number of samples to run'
    )
    parser.add_argument(
        '--hidden_rate', '-hr', type=float, default=0.5, 
        help='Proportion of MI scores to hide'
    )
    parser.add_argument(
        '--eval_set', '-e', type=str, default='test',
        choices=['test', 'valid']
    )
    parser.add_argument(
        '--dataset', type=str, default='first', choices=['first', 'all']
    )
    args = parser.parse_args()
    
    # train!
    results = train(args)

    output_filename = f"{args.model_type}{args.n_components if args.model_type != 'clt' else ''}"
    with open(f'../data/{output_filename}_results.json', 'w') as f:
        json.dump(results, f, indent=4)
