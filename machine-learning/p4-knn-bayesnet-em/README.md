## Part 1

To run K-means five times for each value of K, run the two following commands (each for one image). The compressed images will be saved into part1.

```bash
cd part1 # cd into part1/

# Compress Koala image
bash batch-compress.sh Koala.jpg koala-compress

# Compress Penguins image
bash batch-compress.sh Penguins.jpg peng-compress
```

To plot the figures like in my report, use `part1/plot.py` (instructions of cmd arguments are in the code).

## Part 2 

First, make sure you are at the top folder (`p4`) again. Now prepare the data

```bash
# unzip project4.zip into the data folder
unzip project4.zip -d data

# unzip the data of part 2 into `data/project4/part2/dataset`
unzip data/project4/part2/datasets.zip -d data/project4/part2/dataset
```

Run the models and get results. The results will be saved in the `data/` folder.
```bash
cd part2

# Single CLT
python train.py clt --dataset all

# Mixture of CLTs with EM
N_COMPONENTS=5 # assign the number of components for the mixture
python train.py mixture --dataset all --n $N_COMPONENTS

# Random Forest of CLTs
python train.py forest --dataset all -n 8 -hr 0.1
```
