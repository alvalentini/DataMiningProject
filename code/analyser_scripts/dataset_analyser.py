# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 12:51:23 2018

@author: damiano
"""
import common_functions as cf
import numpy as np
import pandas as pd
import matplotlib as plt

tweets, text_tweets = cf.parse('../data/tweets_2xuser_A.txt')
users_tweets = {}
for tweet in tweets:
    user = tweet.user
    if not user in users_tweets:
        users_tweets[user] = 1
    else:
        users_tweets[user] += 1
tweets_per_user = list(users_tweets.values())

df = pd.DataFrame(tweets_per_user)
df_count = df.groupby(0).size().to_frame('grouped')
df_count['grouped'] = df_count['grouped']
plot = df_count.plot.line(by='grouped', legend=False)
#plot.set_yscale('log')
plot.set_ylim(0)
plot.set_xlabel("Tweets per user")
plot.set_ylabel("Number of users")


fig = plot.get_figure()
fig.savefig('./../tweets_per_user_distribution_line-tweets_2xuser_A.png', bbox_inches='tight', dpi = 900)
