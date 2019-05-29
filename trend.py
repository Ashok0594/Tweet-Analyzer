''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 25, 2018
Module name     : trend.py
Description     : This module is to plot a tend of polarity if the searchmade by the user versus
                  the timestamp 
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# import necessary libraries
import matplotlib.pyplot as plt
import DB_Operations
from pylab import *
import pylab
import os

#Plot the trend of polarity for a search term in the timeperiod when searched for multiple instances
def graph(m_id,term):
        plt.close("all")
        savepath = os.path.join("./charts", term+"Trend%d"%m_id)

        #initialize the lists
        s=[]
        search = []

        # get the data from DB
        result_set = DB_Operations.select_polarity(m_id)

        # put the data into lists
        for i in result_set:
            s.append(i[1])
        for i in range(0,len(result_set)):
            c=result_set[i][2].strftime("\n%H:%M %d-%m-%y")
            search.append(c)

        t = arange(-1.0, 1.0, 0.25)

        # plot the values
        pylab.plot(search, s,color = 'g')

        # plot attributes and lables 
        pylab.xlabel('search time')
        pylab.xticks(rotation=90)
        pylab.ylabel('Average polarity')
        pylab.tight_layout()
        pylab.title('%s: Average Polarity Vs Time of Search'%term)
        plt.savefig(savepath, dpi=300)
        plt.draw()
        plt.ion()
        plt.get_current_fig_manager().window.wm_geometry("+1250+250")
        pylab.show()
# end of graph

