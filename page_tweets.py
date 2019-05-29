''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 18, 2018
Module name     : page_tweets.py
Description     : This module inserts the latest 25 tweet posted by the individual
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# import necessary libraries
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from textblob import TextBlob
from tweepy import Stream
import DB_Operations
import tgtrend
import tweepy
import sys
import json

# method for removing Non-BMP characters
def BMP(s):
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))
# end of method BMP
def main(p_id):
    # values for connecting to twitter API
    consumer_key = 'nqWXYHpmgOYIx3OiiNFnydMDz'
    consumer_secret = 'tedYkIBNDe1xiYs6BFszssNy9fTqu3zPpOKpD2tnbp1kHeTGd2'
    access_token = '91548577-zkA8soUyHdxP1TH6yLteTfLB0AELAyXRSHhFC6p0x'
    access_secret = 'mwJBGH49NgmqhVOyhoo102fzavntPBewCdzU7ZzEEdUAx'
     
    # Connect to Twitter API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    if p_id==1:
        name ='microsoft'
    elif p_id==2:
        name ='google'
    elif p_id==3:
        name='twitter'
    elif p_id==4:
        name='IBM'
    elif p_id==5:
        name='illinoistech'
    else :
        name='Gowrishankar_16'
    # Get the tweets from the page
    j=0
    i=25
    DB_Operations.truncate_pages_tweet()

    #For loop to pick the last 25 tweets posted and insert into db
    for tweet in tweepy.Cursor(api.user_timeline,id=name).items():
        a = str(tweet.in_reply_to_user_id)
        if a == 'None':

            if (j<i):
                r_id = tweet.id
                r_text = BMP(tweet.text)
                r_created_at = tweet.created_at
                r_favorite_count = tweet.favorite_count
                r_retweet_count = tweet.retweet_count

                DB_Operations.insert_pages_tweet(p_id,r_id,r_text,r_created_at,r_favorite_count,r_retweet_count)
                
                j += 1
            else:
                break
    tgtrend.main()

