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
    args = parser.parse_args()
    distance = args.distance[0]
    min_size = args.min_cluster_size[0]
    tweets_len = args.tweets_number[0]

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
    cf.evaluation(cluster, tweets)

    # Print configuration
    print()
    print('initial number of tweets =', tweets_len)
    print('distance =', distance)
    print('cluster min size =', min_size)

if __name__ == "__main__":
    # execute only if run as a script
    main()
