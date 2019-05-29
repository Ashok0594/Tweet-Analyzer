''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 21, 2018
Module name     : tgtrend.py
Description     : This module plots the trend of the likes and replies for the last 25 tweets
                  posted by the user,it recollects te tweets from database inserted
                  by the  pages_tweet module
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# import necessary libraries
import DB_Operations
from pylab import *
import os

#Function has the statements for plotting the trend gragh by reading data from database
def main():
    plt.close('all')

    # initialize the lists
    id=[]
    fav = []
    rt=[]
    result_set = DB_Operations.select_pages_tweet()

    # store the values in the list from the result set
    for i in result_set:
        id.append(i[0])
        fav.append (i[1])
        rt.append (i[2])
        ids=i[3]
    # end of for

    # plot the lists as a trendline
    savepath = os.path.join("./charts", "tgtrend%d"%ids)
    plt.plot(id,fav,color='goldenrod',marker='.', linewidth=1, label="LIKES")
    plt.plot(id,rt,color='darkslategray',marker='.', linewidth=1, label="RETWEET")
    plt.legend()

    # lables, titles and plot attributes 
    xlabel('Tweets')
    ylabel('Count')
    title('Favourites and Retweets for the latest 25 tweets')
    plt.savefig(savepath, dpi=300)
    plt.draw()
    plt.ion()
    plt.get_current_fig_manager().window.wm_geometry("+1200+250")
    plt.show()
# end of main


