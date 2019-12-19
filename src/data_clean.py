'''
This code block cleans the stored csv tweets data.
'''

import csv
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import nltk


# read in previously stored csv data file
df = pd.read_csv('twitter_data.csv',
                 names=['', 'Tweet id', 'name', '@', 'location', 'description',
                        'url', 'followers', 'friends', 'listed',
                        'geo', 'coordinates', 'place', 'text', 'createdate',
                        'favorites', 'retweets', 'source', 'in_reply_to_status_id'],
                 na_values=['', 'None'], header=0)

# remove geo tag variables from df
df.drop(['', 'geo', 'coordinates', 'place'], axis=1, inplace=True)

# parse source into tuple of url and source name
df.source = df.source.map(lambda s: re.search(r'.*"(http.*)" .*>(.*)<.*', s).groups())

print(df.info())
print("Describe:\n", df.describe())

# get list of English stopwords
sw = nltk.corpus.stopwords.words('english')
# construct regex pattern
pattern = re.compile('\\b({})\\W'.format('|'.join(sw)), re.I)
# remove stopwords fron string and extract words to list
df.text = df.text.map(lambda s: re.sub(pattern, '', s.lower())).map(lambda s: re.findall(r'\w+', s))
# count Frequency
wordfreq = pd.Series(np.concatenate(df.text)).value_counts()
# extract top 50
top50_words = wordfreq.iloc[:49]
# plot bar chart
top50_words.plot.bar(title="Top 50 Most Frequent Words")
plt.xlabel('Words')
plt.ylabel('Frequency')

# influence by followers count
pf = df[['@', 'followers', 'listed', 'favorites', 'retweets']]
# new list for forming dataframe
follow_list, listed_list, fav_list, rt_list = [], [], [], []
# find unique screen names
userset = set(pf['@'])
# loop through unique screen names
for user in userset:
    # sum up tweet individual counts for user
    fav = pf.loc[pf['@'] == user]['favorites'].sum()
    rt = pf.loc[pf['@'] == user]['retweets'].sum()
    rt_len = len(pf.loc[pf['@'] == user]['retweets'])
    # append to list user 'constant' values
    follow_list.append(pf.loc[pf['@'] == user]['followers'].iloc[0])
    listed_list.append(pf.loc[pf['@'] == user]['listed'].iloc[0])
    # append to list sum of tweets values
    fav_list.append(fav)
    rt_list.append(rt/rt_len)

# form dataframe with user as index
user_frame = pd.DataFrame({'followers': follow_list,
                           'retweets to followers ratio':
                           [r / (f+1) for r, f in zip(rt_list, follow_list)]},
                          index=userset).sort_values('followers',
                                                     ascending=False)
# extract top 50 by followers
plot_frame = user_frame.iloc[:49]
# plot bar chart
plot_frame.plot.bar(subplots=True, title="Top 50 Followed Users, Retweet to Followers Ratio")
plt.xlabel('User Screen Name')

plt.show()


'''
Completed basic parsing, removing empty, None variables,
and prints info() and describe() of the dataframe.

'''
