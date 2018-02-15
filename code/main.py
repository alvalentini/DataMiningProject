import utils
import common_functions as cf
import lsh_approach as lsh
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
    parser.add_argument('--lsh-approach', '-lsh', action="store_true")
    parser.add_argument('--use-metadata', '-md', action="store_true")
    parser.add_argument('--user-profiling', '-up', action="store_true")
    parser.add_argument('--topic-relation', '-tr', action="store_true")
    args = parser.parse_args()
    distance = args.distance[0]
    min_size = args.min_cluster_size[0]
    tweets_len = args.tweets_number[0]
    correlation = args.correlation[0]
    lsh_approach = args.lsh_approach
    use_metadata = args.use_metadata
    user_profiling = args.user_profiling
    topic_relation = args.topic_relation

    # Parse tweets
    tweets, t = cf.parse('../data/tweets_2xuser_time_A.txt',
                         tweets_len, use_metadata)
    tweets_len = len(tweets)
    print('len(tweets) =', tweets_len)

    # Clustering
    if lsh_approach:
        T = lsh.clustering(tweets, t, distance, use_metadata)
    else:
        T = utils.clustering(t[0], t[1], t[2], t[3], distance)

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
    if topic_relation:
        c_len = len(clusters)
        topic_relation = []
        relation_map = {}
        for i in range(c_len):
            relation_map[i] = set()
        for i in range(c_len):
            for j in range(i+1, c_len):
                if clusters[i][6] == clusters[j][6] and clusters[i][6] != None:
                    relation_map[i].add(j)
                    relation_map[j].add(i)
                    topic_relation.append((i, j))
                else:
                    r = len(set.intersection(*[set(clusters[i][5]),
                                               set(clusters[j][5])]))
                    if r >= correlation:
                        relation_map[i].add(j)
                        relation_map[j].add(i)
                        topic_relation.append((i, j))
        for i, j in topic_relation:
            print('Cluster:', clusters[i][0])
            print(clusters[i][1])
            print('Cluster:', clusters[j][0])
            print(clusters[j][1])
            print()
        print('Topic relations:', len(topic_relation))
        print()

    # Users profile
    if user_profiling:
        users_profiles = {}
        for i in range(c_len):
            users = clusters[i][5]
            for user in users:
                if user not in users_profiles:
                    users_profiles[user] = (set(), set())
                users_profiles[user][0].add(clusters[i][0])
        for i in range(c_len):
            users = clusters[i][5]
            for user in users:
                if i in relation_map:
                    for j in relation_map[i]:
                        if clusters[j][0] not in users_profiles[user][0]:
                            users_profiles[user][1].add(clusters[j][0])
        for user, values in users_profiles.items():
            print('User:', user)
            print('Clusters:', values[0])
            print('Correlated clusters:', values[1])
            print()

    # Print configuration
    print()
    print('LSH approach (-lsh) =', lsh_approach)
    print('use metadata (-md) =', use_metadata)
    print('initial number of tweets (-n) =', tweets_len)
    print('distance (-d) =', distance)
    print('cluster min size (-s) =', min_size)
    print('min users to correlate clusters (-c) =', correlation)

if __name__ == "__main__":
    # execute only if run as a script
    main()
