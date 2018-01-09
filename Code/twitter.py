import nltk
import re
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
                       'was', 'its', 'per', 'cent', 'able', 'about',
                       'across', 'after', 'all', 'almost', 'also', 'among',
                       'and', 'any', 'are', 'because',
                       'been', 'but', 'can', 'cannot', 'could', 'dear',
                       'did', 'does', 'either', 'else', 'ever', 'every',
                       'for', 'from', 'get', 'got', 'had', 'has', 'have',
                       'her', 'hers', 'him', 'his', 'how', 'however',
                       'into', 'its', 'just', 'least',
                       'let', 'like', 'likely', 'may', 'might', 'most',
                       'must', 'neither', 'nor', 'not', 'off',
                       'often', 'only', 'other', 'our', 'own',
                       'rather', 'said', 'say', 'says', 'she', 'should',
                       'since', 'some', 'than', 'that', 'the', 'their',
                       'them', 'then', 'there', 'these', 'they', 'this', 'tis',
                       'too', 'twas', 'wants', 'was', 'were',
                       'what', 'when', 'where', 'which', 'while', 'who',
                       'whom', 'why', 'will', 'with', 'would', 'yet', 'you',
                       'your', 'retweet', 'fuck',
                       'yall', 'yay', 'youre', 'youve', 'ass', 'factbox',
                       'com', 'retweeting', 'dick', 'fuckin',
                       'shit', 'via', 'fucking', 'shocker', 'wtf', 'hey',
                       'ooh', 'rtamp', 'amp', 'retweet',
                       'fucks', 'fucka', 'bitch', 'wey',
                       'lol', 'smfh'])
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
        if id == 5000:
            break
    return tweets, text_tweets


def jaccard_similarity(a, b):
    x = a.features
    y = b.features
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)


def main():
    tweets, text_tweets = parse('tweets_50k.txt')
    tweets_len = len(tweets)
    print('len(tweets) =', tweets_len)

    T = utils.clustering(text_tweets, 4)

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


if __name__ == "__main__":
    # execute only if run as a script
    main()
