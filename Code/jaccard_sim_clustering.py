import utils
import common_functions as cf
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--distance', '-d', nargs=1, default=[2.0], type=float)
    parser.add_argument('--tweets-number', '-n', nargs=1,
                        default=[5000], type=int)
    parser.add_argument('--min-cluster-size', '-s', nargs=1,
                        default=[5], type=int)
    args = parser.parse_args()
    print(args)
    distance = args.distance[0]
    min_size = args.min_cluster_size[0]
    tweets_len = args.tweets_number[0]
    tweets, text_tweets = cf.parse('../Dataset/tweets.txt', tweets_len)
    tweets_len = len(tweets)
    print('len(tweets) =', tweets_len)

    T = utils.clustering(text_tweets, distance)

    cluster = {}
    for i in range(len(T)):
        if T[i] not in cluster:
            cluster[T[i]] = []
        cluster[T[i]].append(i)

    num = 0
    for k, v in cluster.copy().items():
        if len(v) >= min_size:
            num += 1
            # print('cluster', k, ':')
            # for t in v:
            #     print(t, ':', tweets[t].features)
            # print()
        else:
            cluster.pop(k)

    tweets_num = 0
    clusters = []
    for k, v in cluster.items():
        v_len = len(v)
        tweets_num += v_len
        cluster_tweets = []
        for t in v:
            cluster_tweets.append(tweets[t].features)
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
        clusters.append((k, cluster_words, v_len, dist, 0))

    c_len = len(clusters)
    bugs = 0
    for i in range(c_len):
        for j in range(i+1, c_len):
            sim = utils.similarity(clusters[i][1], clusters[j][1])
            if sim > clusters[i][4]:
                clusters[i] = clusters[i][0], clusters[i][1], clusters[i][2], clusters[i][3], 1/sim
            if sim > clusters[j][4]:
                clusters[j] = clusters[j][0], clusters[j][1], clusters[j][2], clusters[j][3], 1/sim

    for i in range(c_len):
        print('cluster:', clusters[i][0])
        print(clusters[i][1])
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
    print('initial number of tweets', tweets_len)
    print('distance:', distance)
    print('cluster min size:', min_size)
    print('number of clusters:', num)
    print('tweets in the clusters:', tweets_num)
    print('bugs:', bugs)


if __name__ == "__main__":
    # execute only if run as a script
    main()
