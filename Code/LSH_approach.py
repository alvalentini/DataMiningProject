import nltk
import re
import sys
from math import*
import numpy as np
import scipy.cluster.hierarchy as hie
import utils
from scipy.sparse import lil_matrix
#from nltk.stem import PorterStemmer
#from nltk.tokenize import sent_tokenize, word_tokenize
import random 
import sys
import operator


class Tweet:
    def __init__(self, features, id, user):
        self.features = features
        self.id = id
        self.user = user


def stopwords():
    stop_words = nltk.corpus.stopwords.words('english')
    stop_words.extend(['this', 'that', 'the', 'might', 'have', 'been', 'from',
                       'but', 'they', 'will', 'has', 'having', 'had', 'how',
                       'went', 'were', 'why', 'and', 'still', 'his', 'her',
                       'was', 'its', 'per', 'cent', 'a', 'able', 'about', 'am',
                       'across', 'after', 'all', 'almost', 'also', 'among',
                       'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because',
                       'been', 'but', 'by', 'can', 'cannot', 'could', 'dear',
                       'did', 'do', 'does', 'either', 'else', 'ever', 'every',
                       'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he',
                       'her', 'hers', 'him', 'his', 'how', 'however', 'i',
                       'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least',
                       'let', 'like', 'likely', 'may', 'me', 'might', 'most',
                       'must', 'my', 'neither', 'nor', 'not', 'of', 'off',
                       'often', 'on', 'only', 'or', 'other', 'our', 'own',
                       'rather', 'said', 'say', 'says', 'she', 'should',
                       'since', 'so', 'some', 'than', 'that', 'the', 'their',
                       'them', 'then', 'there', 'these', 'they', 'this', 'tis',
                       'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were',
                       'what', 'when', 'where', 'which', 'while', 'who',
                       'whom', 'why', 'will', 'with', 'would', 'yet', 'you',
                       'your', 've', 're', 'rt',  'retweet', 'fuck', 'ya',
                       'yall', 'yay', 'youre', 'youve', 'ass', 'factbox',
                       'com', 'lt', 'th', 'retweeting', 'dick', 'fuckin',
                       'shit', 'via', 'fucking', 'shocker', 'wtf', 'hey',
                       'ooh', 'rtamp', 'amp', 'retweet', 'goooooooooo',
                       'hellooo', 'gooo', 'fucks', 'fucka', 'bitch', 'wey',
                       'sooo', 'helloooooo', 'lol', 'smfh'])
    stop_words = set(stop_words)
    stop_words = [x for x in stop_words if len(x) > 2]
    return stop_words


def normalize_text(text):
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(pic\.twitter\.com/[^\s]+))', '', text)
    text = re.sub('@[^\s]+', '', text)
    text = re.sub('[^a-zA-Z\s]', '', text)
    return text


#add stemming?
def nltk_tokenize(stop_words, text):
    tokens = []
    features = []
    tokens = text.split()
    #ps = PorterStemmer()
    for word in tokens:
        if word.lower() not in stop_words and len(word) > 2:
            #word = re.sub(r'(.)\1+', r'\1\1', word)
            #word = word.lower
            #word = ps.stem(word)
            features.append(word.lower())
    return features


def parse(filename):
    file_object = open(filename, 'r')
    tweets = []
    text_tweets = []
    stop_words = stopwords()
    id = 0
    for line in file_object:
        username, text = line.split('\t\t')
        text = normalize_text(str(text))
        features = nltk_tokenize(stop_words, text)
        tweet = Tweet(features, id, username)
        if len(features) > 0:
            tweets.append(tweet)
            text_tweets.append(features)
            id = id+1
        # if id == 5000:
        #     break
    return tweets, text_tweets


def dictionary_creation(tweets):
    count = 0
    words = {}    
    for tweet in tweets:
        for word in tweet.features:
            if not word in words:
                words[word] = count
                count = count + 1
    return words
            
            
def initialize_matrix(tweets, words):
    matrix = lil_matrix((len(words), len(tweets)), dtype=int)
    for tweet in tweets:
        for word in tweet.features:
            matrix[words[word], tweet.id]=1
    return matrix
    
    
def clean_matrix_from_rare_words(matrix):
    cleaned_matrix = matrix[matrix.getnnz(1)>2]
    return cleaned_matrix

def generate_hashFunctions(n_hashFunctions, n_rows):
    rows_hashes = {}
    for i in range(n_rows):
        random.seed(i)
        rows_hashes[i]=[]
        for j in range(n_hashFunctions):
            rows_hashes[i].append(random.randint(0, n_rows))
            
    return rows_hashes

def generate_signatures(matrix, rows_hashes):
    matrix_csc= matrix.asformat('csc')
    n_tweets = matrix.shape[1]
    n_words = matrix.shape[0]
    n_hashes = len(rows_hashes[0])
    signature_matrix = np.full([n_hashes, n_tweets], sys.maxsize)
    for tweet in range(n_tweets):
        tweet_words = matrix_csc.getcol(tweet).nonzero()[0]        
        for word in tweet_words:
            # useless control..
            if matrix[word, tweet]==1:
                for hash_index in range(n_hashes):
                    hash_value = rows_hashes[word][hash_index]
                    if hash_value < signature_matrix[hash_index, tweet]:
                        signature_matrix[hash_index, tweet] = hash_value
            if matrix[word, tweet]==0:
                print ("THERE IS SOMETHING WRONG" + str(tweet))
        if tweet%100==0:
            print ("i finished computing minhash of tweet number:" + str(tweet))
    return signature_matrix
                
   
    
def main():
    tweets, text_tweets = parse('tweets_50k.txt')
    print('len(tweets) =', len(tweets))

    words = dictionary_creation(tweets)

    matrix = initialize_matrix(tweets, words)
    #matrix = clean_matrix_from_rare_words(matrix)
   
    n_hashFunctions = 100
    rows_hashes = generate_hashFunctions(n_hashFunctions, matrix.shape[0])
    signature_matrix = generate_signatures(matrix, rows_hashes)
    #signature_matrix = generate_signatures_with_sorted_rows(matrix, rows_)
    #signature_matrix = compute_minHash(matrix, hashIterations)

    
if __name__ == "__main__":
    # execute only if run as a script
    main()




# NOTE: obsolete function, minhash is here implemented without the approximation trick   
def compute_minHash(matrix, hashIterations):
    n_tweets = matrix.shape[1]
    n_words = matrix.shape[0]
    #matrix = matrix.asformat('lil')
    signature_matrix = np.zeros((hashIterations, n_tweets), dtype='int')
    for row in range(hashIterations):
        permutation = np.random.permutation(n_words)
        for col in range(n_tweets):
            i = 0
            while i<len(permutation) and matrix[permutation[i], col]==0:
                i += 1        
            # if the tweet contains only rare words which have been removed, we mark it with -1    
            if i==len(permutation):
                signature_matrix[row, col] = -1
            else:
                signature_matrix[row, col] = i
                
            if col%100==0:
                print (col)

        print ("hash number:" + str(row))   
    return signature_matrix
    
    
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