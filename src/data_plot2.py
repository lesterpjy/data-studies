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
df1 = pd.read_csv('user_data/influencer.csv',
                 names=['i', 'name', 'tag', 'location', 'description',
                        'url', 'followers', 'friends', 'listed',
                        'geo', 'coordinates', 'place', 'text', 'createdate',
                        'favorites', 'retweets', 'source', 'm'],
                 na_values=['', 'None'], header=0)

df2 = pd.read_csv('user_data/practitioner.csv',
                 names=['i', 'name', 'tag', 'location', 'description',
                        'url', 'followers', 'friends', 'listed',
                        'geo', 'coordinates', 'place', 'text', 'createdate',
                        'favorites', 'retweets', 'source', 'm'],
                 na_values=['', 'None'], header=0)

df3 = pd.read_csv('user_data/organization.csv',
                 names=['i', 'name', 'tag', 'location', 'description',
                        'url', 'followers', 'friends', 'listed',
                        'geo', 'coordinates', 'place', 'text', 'createdate',
                        'favorites', 'retweets', 'source', 'm'],
                 na_values=['', 'None'], header=0)


# remove geo tag variables from df
df1.drop(['geo', 'coordinates', 'place'], axis=1, inplace=True)

# parse source into tuple of url and source name
df1.source = df1.source.map(lambda s: re.search(r'.*"(http.*)" .*>(.*)<.*', s).groups())

print(df1.info())
print("Describe:\n", df1.describe())


# get list of English stopwords
sw = nltk.corpus.stopwords.words('english')
# construct regex pattern
pattern = re.compile('\\b({})\\W'.format('|'.join(sw)), re.I)
# remove stopwords fron string and extract words to list
df1.text = df1.text.map(lambda s: re.sub(pattern, '', s.lower())).map(lambda s: re.findall(r'\w+', s))
df2.text = df2.text.map(lambda s: re.sub(pattern, '', s.lower())).map(lambda s: re.findall(r'\w+', s))
df3.text = df3.text.map(lambda s: re.sub(pattern, '', s.lower())).map(lambda s: re.findall(r'\w+', s))

# count Frequency
wordfreq1 = pd.Series(df1.text.apply(pd.Series).stack()).value_counts()
wordfreq2 = pd.Series(df2.text.apply(pd.Series).stack()).value_counts()
wordfreq3 = pd.Series(df3.text.apply(pd.Series).stack()).value_counts()


# extract top 50
top50_1 = wordfreq1.iloc[:49]
top50_2 = wordfreq2.iloc[:49]
top50_3 = wordfreq3.iloc[:49]
print(top50_2)

# plot bar chart
label = list(intersect.index)
x = np.arange(len(label))
fig, ax = plt.subplots()

ax.set_ylabel('Frequency')
ax.set_xlabel('Words')
ax.set_xticks(x)
ax.set_xticklabels(label, rotation=90)
ax.bar(x - 0.3, top50_1[0], 0.3, label='followers', color='tab:red')
ax.bar(x, top50_2[0], 0.3, label='followers', color='tab:green')
ax.bar(x + 0.3, top50_3[0], 0.3, label='', color='tab:blue')
plt.title('Top 50 Users by Followers')
plt.legend()
fig.tight_layout()
plt.show()
