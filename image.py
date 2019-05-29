''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 18, 2018
Module name     : image.py
Description     : This module fetches and returns the data for GUI for displaying the
                  details of each twitter user
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# import necessary libraries
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO
import DB_Operations
import tkinter as tk

# main method for processing the core logic
def main(c):
    # get the result set 
    rs=DB_Operations.select_pages_url(c)

    # assign the values from the result set
    URL =rs[6]
    follower=rs[2]
    fav=rs[4]
    lis=rs[3]
    status=rs[5]

    # open url for image and get image
    u = urlopen(URL)
    raw_data = u.read()
    u.close()

    # Official twitter handle links for each page
    if c==4:
        name='@IBM'
        main.link='https://twitter.com/IBM'
    elif c==5:   
        name='@illinoistech'
        main.link='https://twitter.com/illinoistech'
    elif c==1:
        name='@Microsoft'
        main.link='https://twitter.com/Microsoft'
    elif c==3:
        name='@Twitter'
        main.link='https://twitter.com/Twitter'
    elif c==6:
        name='Pixel Tweets'
        main.link='https://twitter.com/Gowrishankar_16'
    else:
        name='@Google'
        main.link='https://twitter.com/Google'
    return(raw_data,follower,lis,fav,status,name)

# end of main()

def linking():
    return(main.link)
