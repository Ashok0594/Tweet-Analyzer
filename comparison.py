''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 23, 2018
Module name     : comparison.py
Description     : This module plots the comparison bar chartand a table to compare the
                  various values for the tweet pages.
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# import necessary libraries
import matplotlib.pyplot as plt
import DB_Operations
import pandas as pd
import numpy as np
import matplotlib
import os

# Main method to execute the core logic
def main(ids):
    
    plt.close('all')

    # initialize the list value
    nam=[]

    # declare the colormap
    cmap = matplotlib.cm.viridis

    # get data from database for building the data frame
    result_set_d = DB_Operations.select_pages ()

    # define the save path
    savepath = os.path.join("./charts", "Comparison%d"%ids)
    
    
    #!!!!!!! start of segment for generating the bar chart !!!!!!!
    
    # build a data frame using pandas
    # ----------- Values are scaled for comparision---------------------
    df = pd.DataFrame([i[0] for i in result_set_d], columns=['PAGE_ID'])
    df['FOLLOWERS_COUNT'] = [i[1]/1000 for i in result_set_d]               # divide the follower_count by 1000 to scale down
    df['LISTED_COUNT'] = [i[2] for i in result_set_d]
    df['FAV_COUNT'] = [i[3]*10 for i in result_set_d]                       # muliply the fav_count by 10 to scale down
    df['STATUSES_COUNT'] = [i[4] for i in result_set_d]
    df['COPMANIES']= [i[5] for i in result_set_d]

    # build a bar chart using the data frame
    ax=df.plot.barh(xticks=df.index,colormap='summer',rot=0)
    # define the y lable
    ax.set_yticklabels(df.COPMANIES)
    # disable the x lable
    ax.set_xticklabels([])
    
    #!!!!!!! end of segment for generating the bar chart !!!!!!! 

    #!!!!!!! start of segment for generating the table !!!!!!!
    
    # get data from database for building the table
    result_set = DB_Operations.select_pages_table ()
    data = result_set

    # define the columns for the table
    columns = ('FOLLOWERS_COUNT', 'LISTED_COUNT', 'FAV_COUNT', 'STATUSES_COUNT')

    # get the companies name from database
    a=(DB_Operations.select_pages_name ())

    # put the name in a list
    for names in a:
        nam.append(names[0])
    rows = nam

    # put the name in a list
    for d in data:
        follow = d[0]

    # Get shades of colors based on the number of companies
    colors = plt.cm.PuBuGn(np.linspace(0, 0.5, len(rows)))
    n_rows = len(data)

    # Initialize the vertical-offset for the cell_text
    y_offset = np.zeros(len(columns))

    # initialize the cell text for the tables
    cell_text = []
    for row in range(n_rows):
        y_offset = data[row]
        cell_text.append([(x ) for x in y_offset])

    # Reverse colors and text labels to display the last value at the top.
    colors = colors[::-1]

    # Plot the values as table
    plt.table(cellText=cell_text,
                          rowLabels=rows,
                          rowColours=colors,
                          colLabels=columns,
                          loc='bottom')
    
    #!!!!!!! end of segment for generating the table !!!!!!! 

    # Adjust layout to add both table and bar chart
    plt.subplots_adjust(left = 0.2,bottom=0.3)

    # plot attributes
    plt.title('Comparision - Values are scaled in barchart for visualization')
    plt.axis('tight')
    plt.savefig(savepath, dpi=300)
    plt.draw()
    plt.ion()
    plt.get_current_fig_manager().window.wm_geometry("+1200+250")
    plt.show()

# end of main()

