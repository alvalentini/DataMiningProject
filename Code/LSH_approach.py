import numpy as np
from scipy.sparse import lil_matrix
import random
import sys
import operator
import common_functions as cf
import itertools as it
import utils

# from nltk.stem import PorterStemmer
# from nltk.tokenize import sent_tokenize, word_tokenize


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
    

def extract_candidates_from_buckets(buckets):
    candidates=[]
    
    i=0
    for bucket in buckets:
        for hash_list in bucket.values():            
            pairs =list(it.combinations(hash_list,2))
            strings = list()
            for pair in pairs:
                strings.append(";".join(str(x) for x in pair))
            
            candidates += strings
        i+=1
        print ("Bucket " + str(i) + " done")
    candidates_set = set(candidates)
    candidates_list = list(candidates_set)
    return candidates_list
  
def get_candidates_lsh(signature_matrix, b, r, k):
    buckets = []
    n_tweets = signature_matrix.shape[1]
    n_hashes = signature_matrix.shape[0]
    row = 0
    for band in range(b):
        hashtable = {}
        for tweet in range(n_tweets):
            hashvalue = hash(tuple(signature_matrix[row:row+r,tweet])) % k
            if hashvalue in hashtable:
                hashtable[hashvalue].append(tweet)
            else:
                hashtable[hashvalue] = [tweet]
        row += r
        buckets.append(hashtable)
    print ("Buckets done")
    candidates = extract_candidates_from_buckets(buckets)
    print ("LSH finished computing")
    return list(candidates)
    #similarity_threshold = 10
    

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


def main():
    tweets, text_tweets = cf.parse('../Dataset/tweets_50k.txt')
    # tweets = tweets[:5000]
    print('len(tweets) =', len(tweets))

    words = dictionary_creation(tweets)

    matrix = initialize_matrix(tweets, words)
    # matrix = clean_matrix_from_rare_words(matrix)

    n_hashFunctions = 100
    rows_hashes = generate_hashFunctions(n_hashFunctions, matrix.shape[0])
    signature_matrix = generate_signatures(matrix, rows_hashes)
    b = 50
    r = 2
    k = 100000000
    #if b*r==signature_matrix.shape[0]:
    candidates = get_candidates_lsh(signature_matrix, b, r, k)
    T = utils.clustering_lsh(text_tweets, candidates, 7)
    cluster_list = []
    for i in range(len(T)):
        cluster_list.append((i, T[i]))
    cluster_list.sort(key=lambda x: x[1])

    last_t = -1
    for i, t in cluster_list:
        if (t != last_t):
            print()
        print(t, i, tweets[i].features)
        last_t = t

    print('\nnumber of cluster', len(set(T)))
    #else:
    #    print("Wrong b and c parameters")
    
    # signature_matrix = generate_signatures_with_sorted_rows(matrix, rows_)
    # signature_matrix = compute_minHash(matrix, hashIterations)


if __name__ == "__main__":
    # execute only if run as a script
    main()


'''
def generate_orderedHashFunctions(n_hashFunctions, n_rows):
    hashes_to_rows={}
    for h in range(n_hashFunctions):
        random.seed(h)
        hashes_to_rows[h] = []
        for row in range(n_rows):
            hashes_to_rows[h].append((row, random.randint(0, n_rows)))
    for h in hashes_to_rows.keys():
        hashes_to_rows[h].sort(key=operator.itemgetter(1))
    return hashes_to_rows

# USELESS, it takes more time
def generate_signatures_with_sorted_rows(matrix, hashes_to_rows):
    n_tweets = matrix.shape[1]
    n_words = matrix.shape[0]
    n_hashes = len(hashes_to_rows)
    signature_matrix = np.full([n_hashes, n_tweets], sys.maxsize)
    for tweet in range(n_tweets):
        for hash_index in range(n_hashes):
            for pair in hashes_to_rows[hash_index]:
                if matrix[pair[0], tweet]==1:
                    signature_matrix[hash_index, tweet] = pair[1]
                    break
        print ("i have done the tweet number:" + str(tweet))


        for word in rows_hashes:
            if matrix[word, tweet]==1:
                for hash_index in range(n_hashes):
                    hash_value = rows_hashes[word][hash_index]
                    if hash_value < signature_matrix[hash_index, tweet]:
                        signature_matrix[hash_index, tweet] = hash_value
        print ("i have done the tweet number:" + str(tweet))

    return signature_matrix
'''
