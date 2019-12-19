'''
This code block uses tweepy package and consumer keys to access Twitter API.  The code returns a csv file
of Twitter data
'''

# Import necessary packages, OS, TWEEPY, and JSON
import os
import tweepy as tw
import pandas as pd
import inspect
import re
import scraper


practitioner = ['KirkDBorne', 'gp_pulipaka', 'MrDataScience', 'hadleywickham']
influencer = ['MikeQuindazzi', 'Fisher85M', 'HaroldSinnott', 'jblefevre60']
organization = ['analyticbridge', 'Talenter_io', 'rstudio', '_100DaysOfCode']

technologies = ['pytorch', 'rstats', 'javascript', 'reactjs', 'angular']
filename = 'practitioner.csv'
alldf = []

for user in practitioner:
    print('user: ', user)
    search_tag = "from:" + user + " -filter:retweets"
    data_until = "2019-12-1"
    num = 1000
    df = scraper.get_data(filename, search_tag, data_until, num)
    alldf.append(df)

dff = pd.concat(alldf, ignore_index=True)
print(dff)
with open(filename, 'a') as f:
    dff.to_csv(f, header=False)
