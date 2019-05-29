''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 18, 2018
Module name     : scatterplot.py
Description     : This module is to plot the polarity for the tweets read  based on the follower count 
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# import necessary libraries
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import DB_Operations
import numpy as np
import matplotlib
import math
import os

#method to plot the scatter plot 
def main(searchterm,s_id):
    plt.close('all')
    savepath = os.path.join("./charts", searchterm+"scatterplot%d"%s_id)
    cmap = matplotlib.cm.viridis
    #cmap = matplotlib.cm.RdYlGn

    #initialize list values
    follow = []
    polarity = []
    volume = []

    # read the database and get the polarity and the followers count
    result_set = DB_Operations.select_user(s_id)

    # read thro the result set and append it to the list
    for tweet in result_set:
        follow.append(tweet[1])
        polarity.append(tweet[2])

    # Calculate the volume factor which determines the size of the circles - scaled to the maximum followers
    dem = max(follow)
    for i in follow:
        volume.append((i/dem)*500)

    # Assign values to plot the scatterplot
    x=follow
    y=polarity
    v=volume
    N=len(follow)

    # Decide the color density based on the polarity of the tweet
    norm = matplotlib.colors.Normalize(vmin=min(y), vmax=max(y))
    colors = [cmap(norm(value)) for value in y]
    area = v

    # plot the scattterplot
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.ylim(-1,1)

    # add a legend for user count
    img = plt.imshow([y], cmap=cmap)
    img.set_visible(False)
    plt.colorbar(img, orientation="vertical", shrink=0.96)

    # plot values for layout and texts
    plt.title("Reach of the Tweet sentiment",family='Calibri',fontsize=15,fontweight="bold",color='olive')
    plt.axis('tight')
    plt.savefig(savepath, dpi=300)
    plt.tight_layout()
    plt.draw()
    plt.ion()
    plt.get_current_fig_manager().window.wm_geometry("+1200+250")  
    plt.show()
# end of main
