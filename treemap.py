''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 22, 2018
Module name     : treemap.py
Description     : This module is to plot a treemap that shows the count of the devices used for posting
                  the tweets.
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# import necessary libraries
import matplotlib.pyplot as plt
import DB_Operations
import pandas as pd
import matplotlib
import squarify    # pip install squarify (algorithm for treemap)
import os

def main(searchterm,s_id):
    plt.close('all')
    #define the color used for the treemap values
    cmap = matplotlib.cm.viridis
    savepath = os.path.join("./charts", searchterm+"treemap%d"%s_id)

    # get the data from database for the specific search
    result_set = DB_Operations.select_source(s_id)

    #build a data frame using pandas
    df=pd.DataFrame(result_set)

    #add heading to the data frame
    df = pd.DataFrame([i[0] for i in result_set], columns=['Source'])
    df['Count'] = [i[1] for i in result_set]
    df['Label'] = df['Source'] + "\n(" + df['Count'].astype("str") + ")"

    # Decide the color density based on the number of users
    norm = matplotlib.colors.Normalize(vmin=min(df.Count), vmax=max(df.Count))
    colors = [cmap(norm(value)) for value in df.Count]

    # set the background color, size of the frame
    fig = plt.gcf()
    fig.set_facecolor('whitesmoke')
    ax = fig.add_subplot()
    fig.set_size_inches(6.5, 5.5)

    # add a legend for user count
    img = plt.imshow([df.Count], cmap=cmap)
    img.set_visible(False)
    fig.colorbar(img, orientation="vertical", shrink=.96)
    fig.text(.78, .87, "Users", family='Calibri',fontsize=12,fontweight="bold",color='olive')

    # build the treemap
    squarify.plot( sizes=df.Count, label=df.Label, color = colors, alpha=.6 )

    #add headings to the plot and set the plot attributes
    plt.title("Source of Tweets",family='Calibri',fontsize=15,fontweight="bold",color='olive')
    plt.axis('off')
    plt.savefig(savepath, dpi=300)
    plt.draw()
    plt.ion()
    plt.get_current_fig_manager().window.wm_geometry("+1200+250")   
    plt.show()
# end of main
