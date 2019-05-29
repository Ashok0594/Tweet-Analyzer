''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 18, 2018
Module name     : users.py
Description     : This module inserts the details of the twiiter account into the database 
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# import necessary libraries
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import DB_Operations
import tweepy
import json
import sys

# method for removal of non-BMP characters
def BMP(s):
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in status.text))
# end of BMP

# main function
def main():

        # twitter connection details 
        consumer_key = 'nqWXYHpmgOYIx3OiiNFnydMDz'
        consumer_secret = 'tedYkIBNDe1xiYs6BFszssNy9fTqu3zPpOKpD2tnbp1kHeTGd2'
        access_token = '91548577-zkA8soUyHdxP1TH6yLteTfLB0AELAyXRSHhFC6p0x'
        access_secret = 'mwJBGH49NgmqhVOyhoo102fzavntPBewCdzU7ZzEEdUAx'

        # Authenticate the keys and establish connection 
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)

        # declare the pages for whcih data needs to be taken
        pages_name = ['microsoft','google','twitter','IBM','illinoistech','Gowrishankar_16']
        
        # The Twitter user who we want to get tweets from
        DB_Operations.truncate_pages()
        
        # Number of tweets to pull
        tweetCount = 20
        p_id = 1
        for name in pages_name:
            # Calling the user_timeline function with our parameters
            results = api.get_user(id=name, count=1)

            # assigning the result set values
            r_id = results.id
            r_name = results.name
            r_location = results.location
            r_followers_count = results.followers_count
            r_listed_count = results.listed_count
            r_favourites_count = results.favourites_count
            r_statuses_count = results.statuses_count
            r_profile_image_url_https = results.profile_image_url_https

            # DB operation to insert the new records
            DB_Operations.insert_pages (p_id,r_id ,r_name,r_location,r_followers_count,r_listed_count,r_favourites_count,r_statuses_count,r_profile_image_url_https)
            p_id +=1

# end of main
