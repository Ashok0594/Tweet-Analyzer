''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 18, 2018
Module name     : posttweet.py
Description     : This module allows individual to post a tweet directly from the GUI
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# import necessary libraries
from tkinter import messagebox
import tweepy

#Main method connects with twitter api and posts the content recieved from the GUI
def main(content):
    consumer_key ="nqWXYHpmgOYIx3OiiNFnydMDz"
    consumer_secret ="tedYkIBNDe1xiYs6BFszssNy9fTqu3zPpOKpD2tnbp1kHeTGd2"
    access_token ="91548577-zkA8soUyHdxP1TH6yLteTfLB0AELAyXRSHhFC6p0x"
    access_token_secret ="mwJBGH49NgmqhVOyhoo102fzavntPBewCdzU7ZzEEdUAx"
     
    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
     
    # authentication of access token and secret
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    if len(content)<140:
        # update the status
        api.update_status(status =content)
        messagebox.showinfo("Sucess", "Tweet posted")
    else:
        messagebox.showinfo("Error", "Tweet exceeds maximum permitted lenght of 140 characters")
# end of main
