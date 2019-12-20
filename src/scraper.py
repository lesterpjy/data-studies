'''
This code block uses tweepy package and consumer keys to access Twitter API.  The code returns a csv file
of Twitter data
'''

# Import necessary packages, OS, TWEEPY, and JSON
import os
import tweepy as tw
import pandas as pd
import inspect

# Defines secret keys and access tokens specific to our Twitter account
consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''

# Sets variables for encryption handling and Authenication
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# INPUT CRITERIA
# Defines search criteria as "#DataScience"
# Defines data range for the search
# Creates file for search results
# Establishes number of items to return during search
search_tag = "#DataScience"
data_until = "2019-11-11"
filename = 'tweet_data.json'
num = 50


def get_data(filename, search_tag, data_until, num):
    '''
    get_data function:
    function takes in filename, search term, date, and number of items to return
    function searches Twitter for given term
    '''

    # call API to return tweets based on input criteria in input section above
    tweets = tw.Cursor(api.search,
                       q=search_tag,
                       lang="en",
                       tweet_mode='extended',
                       until=data_until).items(200)
    # create empty tweet list
    tweetlst = []

    # for each tweet in the search criteria create and fill variables based on json data
    for tweet in tweets:
        # print(inspect.getmembers(tweet, predicate=inspect.ismethod))
        tweet_id = tweet._json['id']
        user = tweet._json['user']  # The user key has a nested dictionary.
        name = user.get('name')
        screen_name = user.get('screen_name')
        location = user.get('location')
        description = user.get('description')
        url = user.get('url')
        followers_count = user.get('followers_count')
        friends_count = user.get('friends_count')
        listed_count = user.get('listed_count')
        geo = tweet._json['geo']
        coordinates = tweet._json['coordinates']
        place = tweet._json['place']
        text = tweet._json['full_text']
        created_at = tweet._json['created_at']
        favorite_count = tweet._json['favorite_count']
        retweet_count = tweet._json['retweet_count']
        source = tweet._json['source']
        in_reply_to_status_id = tweet._json['in_reply_to_status_id']
        # append tweet dictionary to list
        tweetlst.append({'tweet_id': str(tweet_id),
                         'name': str(name),
                         'screen_name': str(screen_name),
                         'location': str(location),
                         'description': str(description),
                         'url': str(url),
                         'followers_count': int(followers_count),
                         'friends_count': int(friends_count),
                         'listed_count': int(listed_count),
                         'geo': str(geo),
                         'coordineates': str(coordinates),
                         'place': str(place),
                         'text': str(text),
                         'created_at': created_at,
                         'favorite_count': int(favorite_count),
                         'retweet_count': int(retweet_count),
                         'source': source,
                         'in_reply_to_status_id': in_reply_to_status_id
                         })
    # create pandas dataframe with the list of tweets and the dictionary keys
    tweet_json = pd.DataFrame(tweetlst, columns=
                              ['tweet_id', 'name', 'screen_name', 'location', 'description',
                               'url', 'followers_count', 'friends_count', 'listed_count', 'geo',
                               'coordineates', 'place', 'text', 'created_at',
                               'favorite_count', 'retweet_count',
                               'source', 'in_reply_to_status_id'])

    # export tweet dataframe as CSV file
    with open('twitter_data.csv', 'a') as f:
        tweet_json.to_csv(f, header=False)


get_data(filename, search_tag, data_until, num)

'''
completed the twitter scrapper.  The twitter scrapper exports twitter information to a csv.
****The next step is to do data cleaning.
****Some field contains interal dictionary with important information that need to be removed from the
internal dictionary out into a the main fields/columns
****Fields must be double checked to see if all important information is captured in each tweet
'''
