"""
Identifies the language of a text file.

Run this to identify language
python identify_language.py [-h] [-t TOL] [-f FILE]

version 14.3

- Najim Islam
"""

from argparse import ArgumentParser
from collections import defaultdict
from math import sqrt
from operator import itemgetter
from os import listdir
from os.path import splitext


def main():
    options = Options()
    for rank in classify_doc(options.file, options.tolerance):
        print(f"{rank[0]:17}: {rank[1]:>6.1%}")


class Options:
    """Parse and contain command-line arguments."""

    def __init__(self):
        parser = ArgumentParser(
            description="Identifies the language of a text file")
        parser.add_argument('-t', '--tol', type=int, default=3,
                            help='Tolerance to tune results')
        parser.add_argument('-f', '--file', type=str, default='text.txt',
                            help='File to identify language')
        args = parser.parse_args()
        self.file = args.file
        self.tolerance = args.tol


def classify_doc(document, tolerance):
    """Ranks document by language probability."""

    probability = score_document(document, tolerance)
    return sorted(sorted(probability.items(), key=itemgetter(0)), key=itemgetter(1), reverse=True)


def score_document(document, tolerance):
    """Scores document by normalized dot product."""

    lang_counts = train_classifier(tolerance)
    f = open(document, encoding="utf-8")
    data = f.read()
    n_grams = count_n_grams(data, tolerance)
    score = defaultdict(float)
    for language in lang_counts:
        dot_product = 0
        for gram in n_grams.keys():
            dot_product += lang_counts[language][gram]*n_grams[gram]
        score[language] = dot_product
    f.close()
    return find_probability(score)


def train_classifier(tolerance):
    """Finds txt files in the training set as a string and
    returns a dictionary of normalize n-gram counts per language."""

    n_gram_dict = defaultdict(str)
    directory = "./languages/"
    extention = ".txt"
    for filename in listdir(directory):
        if filename.endswith(extention):
            f = open(directory+filename, encoding="utf-8")
            sample = f.read()
            n_grams = count_n_grams(sample, tolerance)
            n_gram_dict[splitext(filename)[0]] = n_grams
            f.close()
    return n_gram_dict


def count_n_grams(document, tolerance):
    """Takes a string and returns a dictionary of the counts
    of normalized n-grams within the document."""

    n_grams = defaultdict(float)
    for i in range(len(document)-tolerance-1):
        n_grams[document[i:i+int(tolerance)]] += 1
    return normalize(n_grams)


def normalize(counts_dict):
    """Takes a dictionary of n-gram counts and normalizes it by it's length."""

    mag = sqrt(sum([x**2 for x in counts_dict.values()]))
    if not mag:
        mag = 1
    return defaultdict(int, {key: value/mag for (key, value) in counts_dict.items()})


def find_probability(score):
    """Finds confidence level using language probability."""

    total = sum(x for x in score.values())
    if not total:
        total = 1
    return {key: value/total for (key, value) in score.items()}


if __name__ == '__main__':
    main()
