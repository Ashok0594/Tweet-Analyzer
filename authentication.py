''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 10, 2018
Module name     : authentication.py
Description     : This module authenticates the keys provided and connects to Twitter API
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# import the necessary libraries
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from textblob import TextBlob
from tweepy import Stream
import tweepy

class authentication:

    # assign the key values
    def __init__(self):
        consumer_key = 'nqWXYHpmgOYIx3OiiNFnydMDz'
        consumer_secret = 'tedYkIBNDe1xiYs6BFszssNy9fTqu3zPpOKpD2tnbp1kHeTGd2'
        access_token = '91548577-zkA8soUyHdxP1TH6yLteTfLB0AELAyXRSHhFC6p0x'
        access_secret = 'mwJBGH49NgmqhVOyhoo102fzavntPBewCdzU7ZzEEdUAx'

    #return the consumer_key
    def getconsumer_key(self):
        return self.consumer_key
        
    #return the consumer_key
    def getconsumer_secret(self):
        return self.consumer_secret
    
    #return the consumer_key
    def getaccess_token(self):
        return self.access_token
    
    #return the consumer_key
    def getaccess_token_secret(self):
        return self.access_token_secret

# end of class authentication
