''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 18, 2018
Module name     : sentiment.py
Description     : This module plots the sentiment pie chart for the tweet based on topic selected
                  or entered  by the user
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from matplotlib.pyplot import ion, show
import matplotlib.pyplot as plt
import sys,tweepy,csv,re,json
from textblob import TextBlob
import DB_Operations
import matplotlib
matplotlib.use("TkAgg")
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
            plt.close("all")
            savepath = os.path.join("./charts", searchTerm+"sentiment%d"%ids)
            labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                      'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
            sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
            colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
            patches, texts = plt.pie(sizes, colors=colors, startangle=90)
            plt.legend(patches, labels, loc="best")
            plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
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

        result_set = DB_Operations.select_stream(s_id)
        count_terms = DB_Operations.count_stream(s_id)
        NoOfTerms = count_terms [0][0]
        #print(rs)
        for text in result_set :
            c_polarity = float(text[1])
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

        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")
        SentimentAnalysis.plotPieChart(s_id,positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)
# end of class SentimentAnalysis
        
#Function that passes the id of the search term on whose tweets the pie chart is to be made
def main(search_id,term):
    s_id = search_id
    global searchTerm
    searchTerm = term
    #global NoOfTerms
    #NoOfTerms = 100
    #s_id = 18
    SentimentAnalysis.data_stream(s_id)
# end of main
