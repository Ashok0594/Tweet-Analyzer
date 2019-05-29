''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 18, 2018
Module name     : wordcloud.py
Description     : This module plots the wordcloud based on the content from the tweets read for the
                  search term input by the user 
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# imprt necessary libraries
from wordcloud import WordCloud, STOPWORDS
from matplotlib.pyplot import ion, show
import matplotlib.pyplot as plt
from scipy.misc import imread
import matplotlib
matplotlib.use("TkAgg")
import warnings
import os

#Method plots wordcloud and saves it to the directory mentioned
def cloud(searchterm,c,ids):
    plt.close('all')
    # save the content as text file
    if c==1:
        text=open('./TXT/streamcloud.txt','r',encoding = 'utf-8')
    elif c==2:
        text=open('./TXT/searchcloud.txt','r',encoding = 'utf-8')
    data=text.read()
    savepath = os.path.join("./charts", searchterm+"wordcloud%d"%ids)
    twitter_mask = imread('./Libraries/twitter_mask.png', flatten=True)
    warnings.simplefilter("ignore", UserWarning)

    # create a word cloud
    worldcloud=WordCloud(font_path="./Libraries/CabinSketch-Bold.ttf",stopwords=STOPWORDS,background_color='white', mode = "RGB", width = 1800, height=1400,mask=twitter_mask).generate(data)

    # plot attributes
    plt.title("Most used words from the analyzed tweets\n\n")
    plt.imshow(worldcloud)
    plt.axis("off")
    plt.savefig(savepath, dpi=300)
    plt.draw()
    plt.ion()
    plt.get_current_fig_manager().window.wm_geometry("+1200+250")    
    plt.show()

# end of cloud
