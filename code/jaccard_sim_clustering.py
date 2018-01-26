import utils
import common_functions as cf
import argparse


def main():
    # Command line parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--distance', '-d', nargs=1, default=[2.0], type=float)
    parser.add_argument('--tweets-number', '-n', nargs=1,
                        default=[5000], type=int)
    parser.add_argument('--min-cluster-size', '-s', nargs=1,
                        default=[5], type=int)
    parser.add_argument('--correlation', '-c', nargs=1,
                        default=[1], type=int)
    args = parser.parse_args()
    distance = args.distance[0]
    min_size = args.min_cluster_size[0]
    tweets_len = args.tweets_number[0]
    correlation = args.correlation[0]

    # Parse tweets
    tweets, text_tweets = cf.parse('../data/tweets_A.txt', tweets_len)
    tweets_len = len(tweets)
    print('len(tweets) =', tweets_len)

    # Clustering
    T = utils.clustering(text_tweets, distance)

    # Remove small clusters
    cluster = {}
    for i in range(len(T)):
        if T[i] not in cluster:
            cluster[T[i]] = []
        cluster[T[i]].append(i)
    for k, v in cluster.copy().items():
        if len(v) < min_size:
            cluster.pop(k)

    # Evaluation
    clusters = cf.evaluation(cluster, tweets)

    # Topic correlation
    c_len = len(clusters)
    topic_relation = []
    for i in range(c_len):
        for j in range(i+1, c_len):
            r = len(set.intersection(*[set(clusters[i][5]),
                                       set(clusters[j][5])]))
            if r >= correlation:
                topic_relation.append((i, j))
    for i, j in topic_relation:
        print('Cluster:', clusters[i][0])
        print(clusters[i][1])
        print('Cluster:', clusters[j][0])
        print(clusters[j][1])
        print()

    # Print configuration
    print()
    print('initial number of tweets (-n) =', tweets_len)
    print('distance (-d) =', distance)
    print('cluster min size (-s) =', min_size)
    print('min users to correlate clusters (-c) =', correlation)

if __name__ == "__main__":
    # execute only if run as a script
    main()
