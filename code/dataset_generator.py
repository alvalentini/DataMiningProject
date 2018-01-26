import os
from random import randint

source_dataset_size = 0
destination_dataset_size = 500000
destination_dataset_name = 'tweets_2xuser.txt'


file_object = open('/mnt/c/Users/Davide/Desktop/tweet_text_02.csv', 'r')
output_line = []

t = {}
tt = {}

for line in file_object:
    line_list = line.split(',')
    length = len(line_list)
    user = ''
    tweet = ''
    for i in range(0, length):
        if i == 1:
            user = line_list[i]
        if i > 1 and i < length - 4:
            tweet += line_list[i]
    if user not in t:
        t[user] = set([])
    t[user].add(tweet)
    
    if source_dataset_size % 10000 == 0:
        print('read', source_dataset_size / 1000, 'k')
    
    
    #output_line.append(user + '\t\t' + tweet[1:-1])
    source_dataset_size = source_dataset_size + 1
    #if (source_dataset_size % 100000 == 0):
    #    print('Reading', int(source_dataset_size / 1000), 'K')
for k, v in t.items():
    if len(v) > 1:
        for tw in v:
            output_line.append(k + '\t\t' + tw[1:-1])

file = open('../data/'+ destination_dataset_name, 'w')

#interval = int(source_dataset_size / destination_dataset_size)
#print('Interval:', interval)

for i in range(0, len(output_line)):
    file.write(output_line[i] + os.linesep)

#for i in range(randint(0, interval), len(output_line)):
#    file.write(output_line[i] + os.linesep)
#    destination_dataset_size = destination_dataset_size - 1
#    i += randint(1, interval) - 1
#    if (destination_dataset_size % 100000 == 0):
#        print('Writing', int(destination_dataset_size / 1000), 'K left')
#    if destination_dataset_size <= 0:
#        break

file.close()