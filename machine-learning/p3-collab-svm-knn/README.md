This code must be run on a UNIX-based machine (such as Linux, MacOS).

## Environments
You must have Python 3.11.

Then install the requirements by running:
```
pip install -r requirements.txt
```


## Part 1
```bash
mkdir data

# unzip the zip file into data/netflix
unzip assets/netflix.zip -d data/netflix

# run the code
python src/part1_matrix.py
```

## Part 2
```bash
# download mnist
python src/download.py

# run the code
python src/part2.py
```

The results will be stored in `out_mnist`.