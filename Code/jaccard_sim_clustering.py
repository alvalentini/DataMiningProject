import utils
import common_functions as cf


def jaccard_similarity(a, b):
    x = a.features
    y = b.features
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)


def main():
    distance = 2
    min_size = 5
    tweets_len = 50000
    tweets, text_tweets = cf.parse('../Dataset/tweets.txt', tweets_len)
    tweets_len = len(tweets)
    print('len(tweets) =', tweets_len)

    T = utils.clustering(text_tweets, distance)

    cluster = {}

    cluster_list = []
    for i in range(len(T)):
        if T[i] not in cluster:
            cluster[T[i]] = []
        cluster[T[i]].append(i)
        # cluster_list.append((i, T[i]))
    # cluster_list.sort(key=lambda x: x[1])

    num = 0
    for k, v in cluster.copy().items():
        if len(v) >= min_size:
            num += 1
            print('cluster', k, ':')
            for t in v:
                print(t, ':', tweets[t].features)
            print()
        else:
            cluster.pop(k)

    tweets_num = 0
    for k, v in cluster.items():
        v_len = len(v)
        tweets_num += v_len
        cluster_tweets = []
        for t in v:
            cluster_tweets.append(tweets[t].features)
        sim = 0
        d = 0
        for i in range(v_len):
            for j in range(i+1, v_len):
                sim += utils.similarity(cluster_tweets[i], cluster_tweets[j])
                d += 1
        dist = d/sim
        print('cluster', k, '->\t', v_len,
              'tweets\tdistanza media', '%.1f' % dist)
        print()

    # last_t = -1
    # for i, t in cluster_list:
    #     if (t != last_t):
    #         print()
    #     print(t, i, tweets[i].features)
    #     last_t = t

    print()
    print('initial number of tweets', tweets_len)
    print('number of clusters:', num)
    print('tweets in the clusters:', tweets_num)


if __name__ == "__main__":
    # execute only if run as a script
    main()
