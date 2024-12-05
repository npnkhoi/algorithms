import nltk
import os
from typing import Dict, List
from nltk.tokenize import word_tokenize
import numpy as np

DATASETS = ['enron1', 'enron2', 'enron4']
ENCODERS = ['bow', 'bernoulli']

def get_examples(dir: str):
    examples = []
    for file in os.listdir(dir):
        with open(os.path.join(dir, file), 'r', encoding='latin-1') as f:
            examples.append(f.read())
    return examples

def vectorize(sentence: str, tok2id: Dict, encoder='bow') -> np.ndarray:
    """
    Returns a vector representation of a sentence
    """
    words = word_tokenize(sentence)
    vector = np.zeros(len(tok2id))
    for word in words:
        if word in tok2id:
            if encoder == 'bernoulli':
                vector[tok2id[word]] = 1
            elif encoder == 'bow':
                vector[tok2id[word]] += 1
    return vector

def batch_vectorize(examples: List[str], tok2id: Dict, encoder='bow') -> np.ndarray:
    vectors = []
    for example in examples:
        vector = vectorize(example, tok2id, encoder)
        vectors.append(vector)
    return np.stack(vectors)

########## Load data ##########

nltk.download('punkt')

vectorized_datsets = {}
for dataset_name in DATASETS:
    # Read all datasets
    text_datasets = {}
    for split in ['train', 'test']:
        text_datasets[split] = {}
        for label in ['ham', 'spam']:
            dir = f'data/{dataset_name}/{split}/{label}'
            text_datasets[split][label] = get_examples(dir)
            print(f'{dataset_name} {split} {label}: {len(text_datasets[split][label])} examples')
    
    # Build vocab
    vocab = set()
    for label in ['ham', 'spam']:
        for example in text_datasets['train'][label]:
            words = word_tokenize(example)
            for word in words:
                vocab.add(word)

    id2tok, tok2id = {}, {}
    for i, token in enumerate(vocab):
        id2tok[i] = token
        tok2id[token] = i

    
    for encoder in ENCODERS:
        # Vectorize the train and test set
        X_train = batch_vectorize(
            text_datasets['train']['ham'] + text_datasets['train']['spam'], 
            tok2id, encoder
        )
        y_train = np.array(
            [0] * len(text_datasets['train']['ham']) + 
            [1] * len(text_datasets['train']['spam'])
        )
        X_test = batch_vectorize(
            text_datasets['test']['ham'] + text_datasets['test']['spam'], 
            tok2id, encoder
        )
        y_test = np.array(
            [0] * len(text_datasets['test']['ham']) + 
            [1] * len(text_datasets['test']['spam'])
        )

        vectorized_datsets[f'{dataset_name}_{encoder}'] = (
            X_train, y_train, X_test, y_test
        )
    
    print(X_train.shape)