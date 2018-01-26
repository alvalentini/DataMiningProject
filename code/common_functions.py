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
                       'lol', 'smfh',
                       'done', 'ugh', 'good', 'okay', 'please', 'dont', 'omg',
                       'thats', 'thing', 'less', 'want', 'ive', 'shits', 'ahw',
                       'hello', 'oki', 'yes', 'try', 'never', 'kool', 'ahah',
                       'stuff', 'gets', 'damn', 'nah', 'nope', 'btw', 'haha',
                       'lmfao', 'cuz', 'umm', 'lolol', 'pls', 'cmon', 'soo',
                       'wow'])
    stop_words = set(stop_words)
    stop_words = [x for x in stop_words if len(x) > 2]
    return stop_words


def normalize_text(text):
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(pic\.twitter\.com/[^\s]+))', '', text)
    text = re.sub('@[^\s]+', '', text)
    text = re.sub('[^a-zA-Z\s]', ' ', text)
    return text


def nltk_tokenize(stop_words, text):
    tokens = []
    features = []
    tokens = text.split()
    for word in tokens:
        word_lower = word.lower()
        word_len = len(word)
        if word_lower not in stop_words and word_len > 2 and word_len < 20 and not bool(re.match('.*(a{3,}|b{3,}|c{3,}|d{3,}|e{3,}|f{3,}|g{3,}|h{3,}|i{3,}|j{3,}|k{3,}|l{3,}|m{3,}|n{3,}|o{3,}|p{3,}|q{3,}|r{3,}|s{3,}|t{3,}|u{3,}|v{3,}|w{3,}|x{3,}|y{3,}|z{3,}).*', word_lower)):
            features.append(word.lower())
    return features


def parse(filename, num=5000):
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
        if len(features) > 2:
            tweets.append(tweet)
            text_tweets.append(features)
            id = id+1
        if id == num:
            break
    return tweets, text_tweets


def evaluation(cluster, tweets):
    tweets_num = 0
    clusters = []

    # Compute the internal average distance
    for k, v in cluster.items():
        v_len = len(v)
        tweets_num += v_len
        cluster_tweets = []
        cluster_users = set([])
        for t in v:
            cluster_tweets.append(tweets[t].features)
            cluster_users.add(tweets[t].user)
        sim = 0
        d = 0
        map = {}
        for i in range(v_len):
            for w in cluster_tweets[i]:
                if w not in map:
                    map[w] = 0
                map[w] += 1
            for j in range(i+1, v_len):
                sim += utils.similarity(cluster_tweets[i], cluster_tweets[j])
                d += 1
        dist = d/sim
        cluster_words = []
        for w, f in map.items():
            if f >= v_len*(2/3):
                cluster_words.append(w)
        clusters.append((k, cluster_words, v_len, dist, 0, cluster_users))

    # Compute the smaller external distance
    c_len = len(clusters)
    for i in range(c_len):
        for j in range(i+1, c_len):
            sim = utils.similarity(clusters[i][1], clusters[j][1])
            if sim > clusters[i][4]:
                clusters[i] = clusters[i][0], clusters[i][1], clusters[i][2], clusters[i][3], 1/sim, clusters[i][5]
            if sim > clusters[j][4]:
                clusters[j] = clusters[j][0], clusters[j][1], clusters[j][2], clusters[j][3], 1/sim, clusters[i][5]

    # Print results
    bugs = 0
    for i in range(c_len):
        print('Cluster:', clusters[i][0])
        print(clusters[i][1])
        print(clusters[i][5])
        print('cluster size:', clusters[i][2])
        print('average internal distance:', '%.1f' % clusters[i][3])
        if clusters[i][4] == 0:
            print('smaller external distance: +inf')
        else:
            if clusters[i][3] > clusters[i][4]:
                bugs += 1
            print('smaller external distance:', '%.1f' % clusters[i][4])
        print()

    print()
    print('Evaluation report:')
    print('number of clusters =', c_len)
    print('tweets in the clusters =', tweets_num)
    print('bugs =', bugs)
    print()

    return clusters
