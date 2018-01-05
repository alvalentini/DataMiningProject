import nltk
import re
from math import*


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
    return stop_words


def normalize_text(text):
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(pic\.twitter\.com/[^\s]+))', '', text)
    text = re.sub('@[^\s]+', '', text)
    text = re.sub('[^a-zA-Z\s]', '', text)
    return text


def nltk_tokenize(text):
    tokens = []
    features = []
    tokens = text.split()
    stop_words = stopwords()
    for word in tokens:
        if word.lower() not in stop_words and len(word) > 2:
            features.append(word.lower())
    return features


def parse(filename):
    file_object = open(filename, 'r')
    tweets = []
    id = 0
    for line in file_object:
        username, text = line.split('\t\t')
        text = normalize_text(str(text))
        features = nltk_tokenize(text)
        tweet = Tweet(features, id, username)
        if len(features) > 0:
            tweets.append(tweet)
        id = id+1
    return tweets


def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)


def main():
    tweets = parse('tweets_50k.txt')
    for tweet in tweets:
        print(tweet.id, tweet.user, tweet.features)


if __name__ == "__main__":
    # execute only if run as a script
    main()
