## Install

First, create a conda environment as follows:
```bash
conda create -n ml python=3.11.4
conda activate ml
```

Then install poetry and the rest of the dependencies:
```bash
pip install poetry
poetry shell
poetry install
```

To run the training code for CNF dataset, do:
```bash
python train.py --dataset cnf --n_jobs 4 # n_jobs can be modified
```

To train for MNIST, do
```bash
python train.py --dataset mnist --n_jobs 4 # n_jobs can be modified
```

The results will be saved in `cnf_output/` and `mnist_output/`, respectively.
