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
df = pd.read_csv('twitter_data_master.csv',
                 names=['i', 'name', 'tag', 'location', 'description',
                        'url', 'followers', 'friends', 'listed',
                        'geo', 'coordinates', 'place', 'text', 'createdate',
                        'favorites', 'retweets', 'source',
                        'in_reply_to_status_id', 'datetime', 'm'],
                 na_values=['', 'None'], header=0)

# remove geo tag variables from df
df.drop(['geo', 'coordinates', 'place'], axis=1, inplace=True)


# parse source into tuple of url and source name
df.source = df.source.map(lambda s: re.search(r'.*"(http.*)" .*>(.*)<.*', s).groups())

print(df.info())
print("Describe:\n", df.describe())
# get list of English stopwords
sw = nltk.corpus.stopwords.words('english')
# construct regex pattern
pattern = re.compile('\\b({})\\W'.format('|'.join(sw)), re.I)

'''
# remove stopwords fron string and extract words to list
df.text = df.text.map(lambda s: re.sub(pattern, '', s.lower())).map(lambda s: re.findall(r'\w+', s))
# count Frequency
print(df.text.apply(pd.Series).stack())
wordfreq = pd.Series(df.text.apply(pd.Series).stack()).value_counts()
# extract top 50
top50_words = wordfreq.iloc[:49]
# plot bar chart
top50_words.plot.bar(title="")
plt.xlabel('Words')
plt.ylabel('Frequency')
'''

# influence by followers count
pf = df[['tag', 'followers', 'listed', 'favorites', 'retweets']]
# new list for forming dataframe
follow_list, listed_list, fav_list, rt_list = [], [], [], []
# find unique screen names
userset = set(pf['tag'])
# loop through unique screen names
for user in userset:
    # sum up tweet individual counts for user
    fav = pf.loc[pf['tag'] == user]['favorites'].sum()
    rt = pf.loc[pf['tag'] == user]['retweets'].sum()
    rt_len = len(pf.loc[pf['tag'] == user]['retweets'])
    fav_len = len(pf.loc[pf['tag'] == user]['favorites'])
    # append to list user 'constant' values
    follow_list.append(pf.loc[pf['tag'] == user]['followers'].iloc[0])
    listed_list.append(pf.loc[pf['tag'] == user]['listed'].iloc[0])
    # append to list sum of tweets values
    fav_list.append(fav/fav_len)
    rt_list.append(rt/rt_len)

# form dataframe with user as index
user_frame = pd.DataFrame({'followers': follow_list,
                           'rf_ratio':
                           [r / (f+1) for r, f in zip(rt_list, follow_list)],
                           'fav_ratio':
                           [fa / (f+1) for fa, f in zip(fav_list, follow_list)]},
                          index=userset).sort_values('followers',
                                                     ascending=False)
# print(user_frame)
pframe = user_frame[(user_frame['rf_ratio'] >= 1)]
pframe = df[df['tag'].isin(pframe.index)]
pframe = pframe.drop_duplicates('tag', keep='first')
print(pframe)

# pframe.text = pframe.text.map(lambda s: re.sub(pattern, '', s.lower())).map(lambda s: re.findall(r'\w+', s))
# # count Frequency
# wordfreq = pd.Series(pframe.text.apply(pd.Series).stack()).value_counts()
# top50_words = wordfreq.iloc[:49]
# # plot bar chart
# top50_words.plot.bar()
# plt.xlabel('Words')
# plt.ylabel('Frequency')
# plt.show()

'''
# extract top 50 by followers
plot_frame = user_frame.iloc[:49]
# plot bar chart
label = list(plot_frame.index)
x = np.arange(len(label))
fig, ax = plt.subplots()

color = 'tab:red'
ax.set_ylabel('Count')
ax.set_xlabel('Users')
ax.set_xticks(x)
ax.set_xticklabels(label, rotation=90)
ax.tick_params(axis='y', labelcolor=color)
ax.bar(x - 0.15, plot_frame['followers'], 0.3, label='followers', color=color)
ax.legend(bbox_to_anchor=(1, 0.9))
ax2 = ax.twinx()

color = 'tab:blue'
ax2.set_ylabel('Value')
ax2.bar(x + 0.15, plot_frame['rf_ratio'], 0.3, label='Average retweet count to followers ratio', color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend()
fig.tight_layout()


fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_ylabel('Count')
ax1.set_xlabel('Users')
ax1.set_xticks(x)
ax1.set_xticklabels(label, rotation=90)
ax1.tick_params(axis='y', labelcolor=color)
ax1.bar(x - 0.15, plot_frame['followers'], 0.3, label='followers', color=color)
ax1.legend(bbox_to_anchor=(1, 0.9))
ax3 = ax1.twinx()

color = 'tab:green'
ax3.set_ylabel('Value')
ax3.bar(x + 0.15, plot_frame['fav_ratio'], 0.3, label='Average favorite count to followers ratio', color=color)
ax3.tick_params(axis='y', labelcolor=color)
ax3.legend()
fig.tight_layout()

plt.show()
'''

'''
Completed basic parsing, removing empty, None variables,
and prints info() and describe() of the dataframe.

'''
