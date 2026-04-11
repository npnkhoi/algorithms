# Bigram Language Model Template

"""
This template will help you build a bigram language model using the NLTK library.
You will preprocess the corpus, build the bigram model, calculate probabilities,
and predict the next words given a sentence prefix.
"""

import nltk
from nltk import bigrams
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
from collections import defaultdict, Counter
import math

# Download required NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('brown')

# Preprocess the corpus: Tokenize, lowercase, and add start/end tokens
def preprocess(corpus):
    """
    Preprocess the corpus by tokenizing, converting to lowercase, and adding <s> and </s> tokens.

    Args:
        corpus (list): List of sentences from the corpus.

    Returns:
        list: Preprocessed and tokenized corpus.
    """
    tokenized_corpus = []
    for sentence in corpus:
        # Tokenize and lowercase the sentence
        # Add '<s>' at the start and '</s>' at the end of the sentence
        lowered = [tok.lower() for tok in sentence]
        lowered = ['<s>'] + lowered + ['</s>']
        tokenized_corpus.append(lowered)
    return tokenized_corpus

# Build the bigram model: Create frequency distributions for unigrams and bigrams
def build_bigram_model(tokenized_corpus):
    """
    Build bigram and unigram frequency distributions.

    Args:
        tokenized_corpus (list): Preprocessed and tokenized corpus.

    Returns:
        tuple: bigram frequencies and unigram frequencies.
    """
    bigram_freq = defaultdict(Counter) # use a two-level dict instead of a tuple-keyed Counter because it is easier to check if a token has been recorded as the first word in a bigram
    unigram_freq = Counter()
    
    for document in tokenized_corpus:
        # Update unigram frequencies
        unigram_freq.update(document)
        # Update bigram frequencies
        for w1, w2 in nltk.bigrams(document):
            bigram_freq[w1].update([w2])
    return bigram_freq, unigram_freq

# Calculate bigram probability with optional smoothing
def bigram_probability(bigram_freq, unigram_freq, word1, word2, smoothing=False):
    """
    Calculate the probability of word2 given word1 using bigram frequencies.
    If smoothing is True, apply Laplace smoothing.

    Args:
        bigram_freq (dict): Bigram frequency distribution.
        unigram_freq (dict): Unigram frequency distribution.
        word1 (str): The preceding word.
        word2 (str): The current word.
        smoothing (bool): Whether to apply Laplace smoothing.

    Returns:
        float: Probability of word2 given word1.
    """
    # TODO: Implement this function
    # HINT:
    # - If smoothing is True, add 1 to the bigram count and adjust unigram count
    # - Vocabulary size V is len(unigram_freq)
    # - Handle cases where counts might be zero to avoid division by zero
    numer = bigram_freq[word1][word2]
    denom = unigram_freq[word1]
    if smoothing:
        numer += 1
        V = len(bigram_freq)
        denom += V
    if denom == 0:
        assert numer == 0
        return 0
    return numer / denom

# Compute the probability of a sentence
def sentence_probability(bigram_freq, unigram_freq, sentence, smoothing=False):
    """
    Compute the probability of a sentence using the bigram model.

    Args:
        bigram_freq (dict): Bigram frequency distribution.
        unigram_freq (dict): Unigram frequency distribution.
        sentence (str): The sentence to compute the probability for.
        smoothing (bool): Whether to apply Laplace smoothing.

    Returns:
        float: Probability of the sentence.
    """
    # Tokenize and lowercase the sentence, add start/end tokens
    # HINT: Use word_tokenize and add '<s>' and '</s>' tokens
    tokens = word_tokenize(sentence)
    tokens = ['<s>'] + [tok.lower() for tok in tokens] + ['</s>']
    # Initialize the probability to 1.0
    # Iterate over the bigrams in the sentence and multiply their probabilities
    # log_prob = 0
    prob = 1.0
    for i in range(len(tokens) - 1):
        # log_prob += math.log(bigram_probability(bigram_freq, unigram_freq, tokens[i], tokens[i+1], smoothing))
        prob *= bigram_probability(bigram_freq, unigram_freq, tokens[i], tokens[i+1], smoothing)

    return prob

# Predict the next N words given a sentence prefix
def predict_next_words(bigram_freq, unigram_freq, sentence_prefix, N, smoothing=False):
    """
    Predict the next N words given a sentence prefix using the bigram model.

    Args:
        bigram_freq (dict): Bigram frequency distribution.
        unigram_freq (dict): Unigram frequency distribution.
        sentence_prefix (str): The sentence prefix.
        N (int): Number of words to predict.
        smoothing (bool): Whether to apply Laplace smoothing.

    Returns:
        str: The predicted next N words.
    """
    # Tokenize and lowercase the sentence prefix
    # HINT: Use word_tokenize
    toks = ['<s>'] + [tok.lower() for tok in word_tokenize(sentence_prefix)] # unnecessary to tokenize the whole thing. Just the last token is enough
    print(f"tokens: {toks}")

    # Initialize current_word with the last word in the prefix
    current_word = toks[-1]

    # For each word to predict:
    # - Check if current_word is in bigram_freq
    # - If it is, find the most frequent next word
    # - If not, break the loop
    # - Append the next word to generated_words
    # - Update current_word
    # - Stop if '</s>' is generated
    ret = ""
    for _ in range(N):
        if current_word == '</s>':
            break

        if not current_word in bigram_freq:
            break
        word, prob = bigram_freq[current_word].most_common(1)[0]
        ret += f" {word}"
        current_word = word
    
    return ret
        

# Main execution
if __name__ == "__main__":
    # Load the corpus
    corpus = brown.sents()
    
    # Preprocess the corpus
    tokenized_corpus = preprocess(corpus)
    
    # Build the bigram model
    bigram_freq, unigram_freq = build_bigram_model(tokenized_corpus)
    print(f"Vocab size: {len(unigram_freq)}")
    
    # Calculate the probability of a test sentence
    test_sentence = "The dog barked at the cat."
    probability_no_smoothing = sentence_probability(bigram_freq, unigram_freq, test_sentence, smoothing=False)
    print(f"Sentence probability without smoothing: {probability_no_smoothing}")
    
    probability_with_smoothing = sentence_probability(bigram_freq, unigram_freq, test_sentence, smoothing=True)
    print(f"Sentence probability with smoothing: {probability_with_smoothing}")
    
    # Predict the next N words
    sentence_prefix = "I won 200"
    N = 5
    # sentence_prefix = "hello"
    # N = 20
    predicted_words = predict_next_words(bigram_freq, unigram_freq, sentence_prefix, N, smoothing=True)
    print(f"Predicted next {N} words: {predicted_words}")

"""
Answer the following questions based on the outputs of your program:

1. Sentence probability without smoothing: 
0.0
2. Sentence probability with smoothing: 
1.7204128298897112e-25
3. Predicted next 5 words:
million dollars . </s>
(it ends early)
"""
