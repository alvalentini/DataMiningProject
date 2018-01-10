import utils
import common_functions as cf


def jaccard_similarity(a, b):
    x = a.features
    y = b.features
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)


def main():
    tweets, text_tweets = cf.parse('../Dataset/tweets.txt')
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
