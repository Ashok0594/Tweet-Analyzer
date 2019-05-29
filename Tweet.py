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
api = tweepy.API(auth)

#class for streaming API
class tweetListener(StreamListener):
    
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
    def on_data(self, data):
        try:
            raw_data = json.loads (data)
            r_search_type = 'Streaming'
            txtfile = open('./TXT/streamcloud.txt', 'a',encoding = 'utf-8')
            #get the values needed to be stored in the database
            r_id = raw_data.get('id')
            r_created_at = raw_data.get('created_at')
            bmp_text = raw_data.get('text')
            r_text = tweetListener.BMP(bmp_text)
            c_text = r_text.encode("utf-8", errors='ignore')
            
            #calculate the polarity
            analysis = TextBlob(r_text)
            r_polarity = analysis.sentiment.polarity
            #get the user details

            #get the user details
            user = raw_data.get('user')
            r_name = user.get('name')
            r_user_id = user.get('id')
            r_source=raw_data.get('source')
            r_source=r_source.replace('<',"").replace('>',"").replace("/a","")
            r_source=r_source.split('nofollow"',1)[1]
            r_followers_count = user.get('followers_count')
            r_statuses_count = user.get('statuses_count')
            r_location = user.get('location')
            r_truncated = raw_data.get('truncated')
            r_favorites_count = raw_data.get('favourite_count')
            
            # insert the data into the database
            DB_Operations.insert_stream (int(r_id),int(r_master_id),int(r_search_id),r_search_type,r_text,r_polarity,r_created_at,r_name,r_user_id,r_followers_count,r_statuses_count,r_location,r_source,r_truncated,r_favorites_count)
            txtfile.write(r_text.replace("https","").replace("RT",""))
            # increment the counter
            self.counter += 1

            # terminate if the number of tweets has been reached
            if self.counter < tweetCount:
                return True
            else:
                self.counter = 0
                twitter_stream.disconnect()
            # end of if
            
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        #end of try except
         
        return True    
    #end of on_data

    # method for errors 
    def on_error(self, status):
        print(status)
        return True
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
    # end of on_error

# call stream listener to get the data
twitter_stream = Stream(auth, tweetListener())

#end of class tweetListener
 
# Get the latest top 5 now trending 'worldwide'
def trending ():
    # put the trends as dictionary 
    now_trend = api.trends_place(23424977) #1 denotes worldwide trends
    data_trends = now_trend[0]
    
    # capture the trends
    trends = data_trends['trends']
    
    # Take only the name of the trends and filter top 5
    names = [trend['name'] for trend in trends]
    
    top5 = names[:5]
    return(top5)

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

    # define the filter consditions fo rthe streaming data    
    twitter_stream.filter(track=[searchTerm],languages=['en'])

    return(r_search_id )
# end of main()

#end of module
