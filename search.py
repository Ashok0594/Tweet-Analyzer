''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 10, 2018
Module name     : Tweet.py
Description     : This module connects to twitter through streaming API and returns the tweets.
                  The tweets are then wrtiten to the database which will then analyze the sentiment
                  of the crowd.
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# import necessary libraries
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from textblob import TextBlob
from tweepy import Stream
import DB_Operations
import sentiment
import wordclod
import tweepy
import json
import sys
import os

# twitter connection details 
consumer_key = 'nqWXYHpmgOYIx3OiiNFnydMDz'
consumer_secret = 'tedYkIBNDe1xiYs6BFszssNy9fTqu3zPpOKpD2tnbp1kHeTGd2'
access_token = '91548577-zkA8soUyHdxP1TH6yLteTfLB0AELAyXRSHhFC6p0x'
access_secret = 'mwJBGH49NgmqhVOyhoo102fzavntPBewCdzU7ZzEEdUAx'

# Authenticate the keys and establish connection 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret) 
api = tweepy.API(auth,wait_on_rate_limit=True)

#class for streaming API
class searchTweets:
    
    # method to initialize
    def __init__(self):
        super().__init__()
        self.counter = 0
        search_flag = 0
        self.limit = 0
        
    # end of __init__
    
    # method for cleaning Non-BMP character 
    def BMP(s):
        return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))
    # end of BMP
   
    # method to get data from twitter
    def search(s_term,n_term):
        
        results = tweepy.Cursor(api.search,q=s_term, lang='en').items(n_term)
        if os.path.exists('./TXT/searchcloud.txt'):
            os.remove('./TXT/searchcloud.txt')
        txtfile = open('./TXT/searchcloud.txt', 'a',encoding = 'utf-8')

        for tweet in results:
            r_search_type = 'Static'
            
            #get the values needed to be stored in the database
            r_id = tweet.id
            r_created_at = tweet.created_at
            bmp_text = tweet.text
            r_text = searchTweets.BMP(bmp_text)
            c_text = r_text.encode("utf-8", errors='ignore')

            #calculate the polarity
            analysis = TextBlob(r_text)
            r_polarity = analysis.sentiment.polarity
            #get the user details

            #get the user details
            
            r_name = tweet.user.name
            r_user_id = tweet.user.id
            r_followers_count = tweet.user.followers_count
            r_statuses_count = tweet.user.statuses_count
            r_location = tweet.user.location
            r_source = tweet.source
            r_truncated = tweet.truncated
            r_favorites_count = tweet.user.favourites_count

            if (not tweet.retweeted) and ('RT @' not in tweet.text):
                txtfile.write(r_text.replace("https","").replace("RT",""))
            DB_Operations.insert_stream (int(r_id),int(r_master_id),int(r_search_id),r_search_type,r_text,r_polarity,r_created_at,r_name,r_user_id,r_followers_count,r_statuses_count,r_location,r_source,r_truncated,r_favorites_count)
        txtfile.close()
        
    # method for errors 
    def on_error(self, status):
        print(status)
        return True
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
    # end of on_error

# call stream listener to get the data


# method for checking and returning MASTER_ID
def check_master():
    #Check if the search term has already been searched
    master_id = DB_Operations.read_master(searchTerm)
    
    #if searched, return the MASTER_ID else insert a new record and return the MASTER_ID
    if not master_id:
        m_id = DB_Operations.insert_master(searchTerm)
        r_master_id = m_id[0][0]

    else:
        r_master_id = master_id[0][0]
    #end of if
        
    return r_master_id
# end of method check_master

# method for inserting and returning SEARCH_ID
def search_master():
    # return back the master_id for inserting
    r_master_id = check_master()
    
    #Add a new record for this search in search log and return back the SEARCH_ID
    DB_Operations.insert_search(r_master_id,searchTerm)            
    s_id = DB_Operations.select_search(r_master_id)     
    r_search_id = s_id[0][0]
    return r_search_id
# end of method search_master

# method for main processing logic
def main(term,count):
    # first get the top trending tweets

    # input from user for the tweet which needs to be searched
    global searchTerm
    searchTerm = term  

    # input from user for the number of tweets 
    global tweetCount
    tweetCount = count

    # strat processing the tweets
    print ("\nInitializing Read...")

    #check for MASTER_ID
    global r_master_id
    r_master_id = check_master()
    
    #check for SEARCH_ID
    global r_search_id
    r_search_id = search_master()

    searchTweets.search(searchTerm,tweetCount)
    return(r_search_id)
    #call the sentiment module to calculate sentiment
    #sentiment.main(r_search_id,searchTerm)
    #wordclod.cloud(searchTerm,2,r_search_id)
# end of main()

global n_term

#end of module
