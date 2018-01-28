import numpy as np
from scipy.sparse import lil_matrix
import random
import sys
import operator
import common_functions as cf
import itertools as it
import utils as ut


def dictionary_creation(tweets):
    count = 0
    words = {}
    for tweet in tweets:
        for word in tweet.features:
            if word not in words:
                words[word] = count
                count = count + 1
    return words


def initialize_matrix(tweets, words):
    matrix = lil_matrix((len(words), len(tweets)), dtype=int)
    for tweet in tweets:
        for word in tweet.features:
            matrix[words[word], tweet.id] = 1
    return matrix


def clean_matrix_from_rare_words(matrix):
    cleaned_matrix = matrix[matrix.getnnz(1) > 2]
    return cleaned_matrix


def generate_hashFunctions(n_hashFunctions, n_rows):
    rows_hashes = {}
    for i in range(n_rows):
        random.seed(i)
        rows_hashes[i] = []
        for j in range(n_hashFunctions):
            rows_hashes[i].append(random.randint(0, n_rows))

    return rows_hashes


def generate_signatures(matrix, rows_hashes):
    matrix_csc = matrix.asformat('csc')
    n_tweets = matrix.shape[1]
    n_words = matrix.shape[0]
    n_hashes = len(rows_hashes[0])
    signature_matrix = np.full([n_hashes, n_tweets], sys.maxsize)
    for tweet in range(n_tweets):
        tweet_words = matrix_csc.getcol(tweet).nonzero()[0]
        for word in tweet_words:
            # useless control..
            if matrix[word, tweet] == 1:
                for hash_index in range(n_hashes):
                    hash_value = rows_hashes[word][hash_index]
                    if hash_value < signature_matrix[hash_index, tweet]:
                        signature_matrix[hash_index, tweet] = hash_value
            if matrix[word, tweet] == 0:
                print("THERE IS SOMETHING WRONG" + str(tweet))
        if tweet % 1000 == 0:
            print("i finished computing minhash of tweet number:" + str(tweet))
    return signature_matrix


def extract_buckets_to_combine(buckets):
    tuples = set()
    for bucket in buckets:
        for hash_list in bucket.values():
            if len(hash_list) > 1:
                tuples.add(tuple(hash_list))
    lists = []
    for t in tuples:
        lists.append(list(t))

    res = []
    for l in lists:
        string_list = []
        for number in l:
            string_list.append(number)
        res.append(string_list)
    return res


def get_candidates_lsh(signature_matrix, b, r, k):
    buckets = []
    n_tweets = signature_matrix.shape[1]
    n_hashes = signature_matrix.shape[0]
    row = 0
    for band in range(b):
        hashtable = {}
        for tweet in range(n_tweets):
            hashvalue = hash(tuple(signature_matrix[row:row+r, tweet])) % k
            if hashvalue in hashtable:
                hashtable[hashvalue].append(tweet)
            else:
                hashtable[hashvalue] = [tweet]
        row += r
        buckets.append(hashtable)
    print("Buckets done")

    return extract_buckets_to_combine(buckets)

    # similarity_threshold = 10


# NOTE: obsolete function, minhash is here
# implemented without the approximation trick
def compute_minHash(matrix, hashIterations):
    n_tweets = matrix.shape[1]
    n_words = matrix.shape[0]
    # matrix = matrix.asformat('lil')
    signature_matrix = np.zeros((hashIterations, n_tweets), dtype='int')
    for row in range(hashIterations):
        permutation = np.random.permutation(n_words)
        for col in range(n_tweets):
            i = 0
            while i < len(permutation) and matrix[permutation[i], col] == 0:
                i += 1
            # if the tweet contains only rare words which
            # have been removed, we mark it with -1
            if i == len(permutation):
                signature_matrix[row, col] = -1
            else:
                signature_matrix[row, col] = i

            if col % 100 == 0:
                print(col)

        print("hash number:" + str(row))
    return signature_matrix


def clustering(tweets, text_tweets, distance):
    words = dictionary_creation(tweets)

    matrix = initialize_matrix(tweets, words)
    # matrix = clean_matrix_from_rare_words(matrix)

    n_hashFunctions = 100
    rows_hashes = generate_hashFunctions(n_hashFunctions, matrix.shape[0])
    signature_matrix = generate_signatures(matrix, rows_hashes)
    b = 50
    r = 2
    k = 1000000000

    candidates_lists = get_candidates_lsh(signature_matrix, b, r, k)

    return ut.clustering_lsh(text_tweets, candidates_lists, distance)
