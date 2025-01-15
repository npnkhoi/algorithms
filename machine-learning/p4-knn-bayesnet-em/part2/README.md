## Part 2 

First, prepare the data

```bash
# unzip project4.zip into the data folder
unzip project4.zip -d data

# unzip the data of part 2 into `data/project4/part2/dataset`
unzip data/project4/part2/datasets.zip -d data/project4/part2/dataset
```

Run the models and get results. The results will be saved in the `data/` folder.
```bash
# Single CLT
python train.py clt --dataset all

# Mixture of CLTs with EM
N_COMPONENTS=5 # assign the number of components for the mixture
python train.py mixture --dataset all --n $N_COMPONENTS

# Random Forest of CLTs
python train.py forest --dataset all -n 8 -hr 0.1
```
