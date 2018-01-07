import nltk
import re
import sys
from math import*
import numpy as np
import scipy.cluster.hierarchy as hie
import utils


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


def nltk_tokenize(stop_words, text):
    tokens = []
    features = []
    tokens = text.split()
    for word in tokens:
        if word.lower() not in stop_words and len(word) > 2:
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


def jaccard_similarity(a, b):
    x = a.features
    y = b.features
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)


def main():
    tweets, text_tweets = parse('tweets_50k.txt')
    print('len(tweets) =', len(tweets))
    distances = []
    distances = utils.distances(text_tweets)
    # for i in range(len(tweets)):
    #     for j in range(i+1, len(tweets)):
    #         sim = jaccard_similarity(tweets[i], tweets[j])
    #         if sim == 0:
    #             distances.append(float(sys.maxsize))
    #         else:
    #             distances.append(1/sim)
    Y = np.array(distances)
    Z = hie.linkage(Y)
    T = hie.fcluster(Z, t=4.0, criterion='distance')
    np.set_printoptions(threshold=np.nan)
    print('len(Y) =', len(Y))
    print('len(T) =', len(T))
    for i in range(len(T)):
        print(i+1, T[i], tweets[i].features)


if __name__ == "__main__":
    # execute only if run as a script
    main()
