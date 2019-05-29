''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 18, 2018
Module name     : in_sentiment.py
Description     : This module plots the sentiment pie chart for the latest tweet posted
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#Import statements for necessary packages used
from tweepy.streaming import StreamListener
from matplotlib.pyplot import ion, show
import matplotlib.pyplot as plt
from tweepy import OAuthHandler
import sys,tweepy,csv,re, json
from tkinter import messagebox
from textblob import TextBlob
from textblob import TextBlob
from tweepy import Stream
import DB_Operations
import matplotlib
matplotlib.use("TkAgg")
import tgtrend
import tweepy
import json
import sys
import os



class SentimentAnalysis:
    #Constructor for the class
    def __init__(self):
        self.tweets = []
        self.tweetText = []
        self.counter = 0
        
    #Function for converting the polarity value into percentage 
    def percentage(part, whole):
            temp = 100 * float(part) / float(whole)
            return format(temp, '.2f')

    #Function that actually plots the pie chart 
    def plotPieChart(ids,positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
            plt.close('all')
            savepath = os.path.join("./charts", "Firm_sentiment%s"%ids)
            labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                      'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
            sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
            colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
            patches, texts = plt.pie(sizes, colors=colors, startangle=90)
            plt.legend(patches, labels, loc="best")
            plt.title('How people are reacting on the recent tweet')
            plt.axis('equal')
            plt.tight_layout()
            plt.savefig(savepath, dpi=300)
            plt.draw()
            plt.ion()
            plt.get_current_fig_manager().window.wm_geometry("+1200+250")
            plt.show()

    def data_stream(s_id):

        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0
        #self.counter = 0

        result_set = DB_Operations.select_reply(s_id)
        if result_set==[]:
            messagebox.showinfo("Error", "No reply available for analysing")
            return 0
        
        
        count_terms = DB_Operations.count_reply(s_id)
        NoOfTerms = count_terms [0][0]
        for text in result_set :

            c_polarity = float(text[0])
            # adding up polarities to find the average later
            polarity += c_polarity

            if (c_polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (c_polarity > 0 and c_polarity <= 0.3):
                wpositive += 1
            elif (c_polarity > 0.3 and c_polarity <= 0.6):
                positive += 1
            elif (c_polarity > 0.6 and c_polarity <= 1):
                spositive += 1
            elif (c_polarity > -0.3 and c_polarity <= 0):
                wnegative += 1
            elif (c_polarity > -0.6 and c_polarity <= -0.3):
                negative += 1
            elif (c_polarity > -1 and c_polarity <= -0.6):
                snegative += 1
        # finding average of how people are reacting

        positive = SentimentAnalysis.percentage(positive, NoOfTerms)
        wpositive = SentimentAnalysis.percentage(wpositive, NoOfTerms)
        spositive = SentimentAnalysis.percentage(spositive, NoOfTerms)
        negative = SentimentAnalysis.percentage(negative, NoOfTerms)
        wnegative = SentimentAnalysis.percentage(wnegative, NoOfTerms)
        snegative = SentimentAnalysis.percentage(snegative, NoOfTerms)
        neutral = SentimentAnalysis.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")

        # call the method for plotting pie chart
        SentimentAnalysis.plotPieChart(s_id,positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)

        
#s_id = 1
def main(r_in_reply_to_status_id_str):
    s_id = r_in_reply_to_status_id_str
    global searchTerm
    searchTerm = 'Replies'
    #global NoOfTerms
    #NoOfTerms = 100
    #s_id = 18
    SentimentAnalysis.data_stream(s_id)

            

def BMP(s):
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))

#Function that reads the latest tweet from twitter picks all the reply for it
def useful(p_id):
    print(p_id)
    val = 'None'
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

    consumer_key = 'nqWXYHpmgOYIx3OiiNFnydMDz'
    consumer_secret = 'tedYkIBNDe1xiYs6BFszssNy9fTqu3zPpOKpD2tnbp1kHeTGd2'
    access_token = '91548577-zkA8soUyHdxP1TH6yLteTfLB0AELAyXRSHhFC6p0x'
    access_secret = 'mwJBGH49NgmqhVOyhoo102fzavntPBewCdzU7ZzEEdUAx'
     
    # Connect to Twitter API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    r_in_reply_to_status_id_str=0
    replies=[] 
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    print (name)
    #Nested for loop to  pick the latest tweet status id  and then retrieve replies from twitter
    for full_tweets in tweepy.Cursor(api.user_timeline,screen_name=name,timeout=999999).items(1):
        for tweet in tweepy.Cursor(api.search,q='to:'+name,result_type='recent',timeout=999999).items(1000):
            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
                    replies.append(tweet.text)

        #For loop to iterate through reading the replies for the latest tweet
        for elements in replies:
            r_p_id = 1
            r_a_tweet = full_tweets.text.translate(non_bmp_map)
            
            r_in_reply_to_status_id_str = tweet.in_reply_to_status_id_str
            val = str(r_in_reply_to_status_id_str)
            r_reply_text = BMP(elements)
            analysis = TextBlob(r_reply_text)
            r_polarity = analysis.sentiment.polarity
            if val != 'None':
                DB_Operations.insert_pages_reply(p_id,r_a_tweet,r_in_reply_to_status_id_str,r_reply_text,r_polarity)
            
            
        replies.clear()

    #If else block to display a message if the latest tweet doesn't have any reply for it
    if val != 'None':
        main(r_in_reply_to_status_id_str)
    else:
        messagebox.showinfo("Oops", "No reply availabele for analysing")

