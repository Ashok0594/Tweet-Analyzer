''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 10, 2018
Module name     : DB_Operations.py
Description     : This module connects to Azure SQL database and performs the query operations
                  based on the parameters passed to the method.
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# import the libraries
from tkinter import messagebox
import hashlib
import pyodbc
import re

# Connection details
server = 'pixel-tweets.database.windows.net'
database = 'pixel'
username = 'pixel'
password = 'Iamlegend94'
driver= '{ODBC Driver 13 for SQL Server}'

#method to connect to Azure SQL
def connection ():
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn
#end of method Connection

# Method to select records from the file TWEET_MASTER
def read_master(term):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #fetch query for TWEET_MASTER
            sql = '''SELECT MASTER_ID FROM TWEET_MASTER WHERE TERM = ? '''
            param = (str(term))
            #execute the sql query
            cursor.execute(sql,param)
            result=cursor.fetchall()
            return (result)
        
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred in SELECT query on TWEET_MASTER - read_master . Rolback sucessful! \nThis record is skipped and processing will continue\n",e)

    cnxn.close()
#end of method read_master

# Method to insert records to the file TWEET_MASTER
def insert_master(term):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            #cnxn.autocommit = True
            cursor = cnxn.cursor()
            #Insert query for TWEET_STREAM
            sql = '''INSERT INTO TWEET_MASTER (TERM) VALUES (?)'''
            param = (str(term))
            #execute the sql query
            cursor.execute(sql,param)
            # commit the changes
            cnxn.commit()
            return(read_master(term))
    
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred on INSERT to TWEET_MASTER - insert_master. Rolback sucessful!\nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method insert_master

# Method to Select tweet and polarity from the file TWEET_STREAM
def select_stream(s_id):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #select query for TWEET_STREAM
            sql = '''SELECT TWEET,POLARITY FROM TWEET_STREAM WHERE SEARCH_ID = ? '''
            param = (str(s_id))
            cursor.execute(sql,param)
            result=cursor.fetchall()
            return (result)
        
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred on SELECT query on TWEET_STREAM - select_stream. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method select_search

# Method to insert records to the file TWEET_STREAM
def insert_stream(id_t,ref_id,ser_id,ser_type,text,pol,created_at,name,user_id,followers,statuses,location,source,truncated,favorite_count):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            #cnxn.autocommit = True
            cursor = cnxn.cursor()
            #Insert query for TWEET_STREAM
            sql = '''INSERT INTO TWEET_STREAM (ID,MASTER_ID,SEARCH_ID,TYPE,TWEET,POLARITY,CREATED_AT,NAME,USER_ID,FOLLOWERS_COUNT,STATUSES_COUNT,LOCATION,TWEET_SOURCE,TRUNCATED,FAV_COUNT) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            param = (int(id_t),int(ref_id),int(ser_id),str(ser_type),str(text),float(pol),str(created_at),str(name),str(user_id),int(followers),int(statuses),str(location),str(source),str(truncated),str(favorite_count))
            #execute the sql query
            cursor.execute(sql,param)
            # commit the changes
            cnxn.commit()
            
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred in INSERT to TWEET_STREAM - insert_stream. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method insert_stream

###############################################################################################################################################
# Method to select records to the file TWEET_SEARCH   
def select_search(m_id):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            # Select query for TWEET_STREAM
            sql = '''SELECT TOP(1) SEARCH_ID FROM TWEET_SEARCH WHERE MASTER_ID = ? ORDER BY SEARCH_ID DESC'''
            param = (str(m_id))
            cursor.execute(sql,param)
            result=cursor.fetchall()
            return (result)
        
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred on SELECT query on TWEET_SEARCH - select_search. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method select_search

# Method to insert records to the file TWEET_SEARCH
def insert_search(m_id,term):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #Insert query for TWEET_STREAM
            sql = '''INSERT INTO TWEET_SEARCH (MASTER_ID,TERM,SEARCH_DATE) VALUES (?,?,CURRENT_TIMESTAMP)'''
            param = (int(m_id),str(term))
            #execute the sql query
            cursor.execute(sql,param)
            #commit the changes
            cnxn.commit()
            
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred on INSERT to TWEET_SEARCH - insert_search. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)
            
    cnxn.close()
#end of method insert_search

# Method to select the count of records from the file TWEET_SEARCH
def count_stream(s_id):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #Insert query for TWEET_STREAM
            sql = '''SELECT COUNT(SEARCH_ID) FROM dbo.TWEET_STREAM WHERE SEARCH_ID=? GROUP BY SEARCH_ID;'''
            param = (str(s_id))
            cursor.execute(sql,param)
            result=cursor.fetchall()
            return (result)
        
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred on SELECT query on TWEET_SEARCH - count_stream. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method count_stream

# Method to select the records from the file LOGIN
def uservalid(name,password):
    cnxn = connection ()
    result =[]
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            cursor.execute("SELECT USER_NAME,PASSWORD FROM LOGIN WHERE USER_NAME=? ",str(name))
            result=cursor.fetchall()
            cnxn.commit()
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            print ("Error occurred on SELECT query on LOGIN - uservalid.  Rolback sucessful! \nThis record is skipped and processing will continue\n",e)          
    cnxn.close()
    if result==[]:
        return('Null','Null')
    else:
        return(result[0][0],result[0][1])
#end of method uservalid

# Method to select and insert the records to the file LOGIN
def sigup(fname,lname,username,password):
    cnxn = connection ()
    d=re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password)
    h = hashlib.md5(password.encode())
    password=h.hexdigest()
    if d:
        c=0
        if cnxn is not None:
            try:
                cursor = cnxn.cursor()
                cursor.execute("SELECT USER_NAME FROM LOGIN WHERE USER_NAME=?",str(username))
                dummy=cursor.fetchall()
                if dummy==[]:
                    cursor.execute("INSERT INTO LOGIN (USER_NAME, FIRST_NAME, LAST_NAME, PASSWORD) VALUES (?,?,?,?)",str(username),str(fname),str(lname),str(password))
                    cnxn.commit()
                    c=1
            except Exception as e:
                # rollback on error
                cnxn.rollback()
                print ("Error occurred on either SELECT or INSERT query on LOGIN - sigup.  Rolback sucessful! \nThis record is skipped and processing will continue\n",e)          
            return(c)
    else:
        messagebox.showinfo("SignUp", "Password should be minimum 8 characters with at least one upper case letter, one special character and one number ")
    cnxn.close()
    
#end of method uservalid

# Method to select records from the file TWEET_MASTER
def getsearchterms():
    cnxn = connection ()
    if cnxn is not None:
         try:
            cursor = cnxn.cursor()
            cursor.execute("SELECT * FROM TWEET_MASTER")
            dummy=cursor.fetchall()
            
         except Exception as e:
            # rollback on error
            cnxn.rollback()
            print ("Error occurred on either SELECT query on TWEET_MASTER - getsearchterms. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)
    cnxn.close()
    return dummy
#end of method getsearchterms

# Method to select records from the file TWEET_SEARCH and TWEET_STREAM
def select_polarity(m_id):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #Select query for TWEET_STREAM and TWEET_STREAM
            sql = '''SELECT A.SEARCH_ID,AVG(A.POLARITY),B.SEARCH_DATE FROM TWEET_STREAM A JOIN TWEET_SEARCH B ON A.SEARCH_ID= B.SEARCH_ID WHERE B.MASTER_ID=? GROUP BY B.SEARCH_DATE,A.SEARCH_ID'''
            param = (str(m_id))
            cursor.execute(sql,param)
            result=cursor.fetchall()
            return (result)
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred on SELECT query on TWEET_SEARCH and TWEET_STREAM - select_polarity. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method select_polarity

# Method to select records from the file TWEET_STREAM
def select_source(s_id):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #Select query for TWEET_STREAM
            sql = '''SELECT TWEET_SOURCE , COUNT(TWEET_SOURCE) FROM TWEET_STREAM WHERE SEARCH_ID = ? GROUP BY TWEET_SOURCE HAVING COUNT(TWEET_SOURCE)> 1 ORDER BY COUNT(TWEET_SOURCE) DESC '''
            param = (str(s_id))
            cursor.execute(sql,param)
            result=cursor.fetchall()
            return (result)
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred on SELECT query on TWEET_SEARCH and TWEET_STREAM - select_source. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method select_source

# Method to select records from the file TWEET_STREAM    
def select_user(s_id):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #select query for TWEET_STREAM
            sql = '''SELECT ID, FOLLOWERS_COUNT, POLARITY FROM TWEET_STREAM WHERE SEARCH_ID = ? and FOLLOWERS_COUNT<10000'''
            param = (str(s_id))
            cursor.execute(sql,param)
            result=cursor.fetchall()
            return (result)
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred on SELECT query on TWEET_STREAM - select_user. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method select_user

# Method to insert records to the file PAGES 
def insert_pages(p_id,r_id ,r_name,r_location,r_followers_count,r_listed_count,r_favourites_count,r_statuses_count,r_profile_image_url_https):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #Insert query for TWEET_STREAM
            sql = '''INSERT INTO PAGES (P_ID ,USER_ID, NAME , LOCATION , FOLLOWERS_COUNT , listed_count , FAV_COUNT , STATUSES_COUNT , profile_image_url_https,CREATE_DATE ) VALUES (?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)'''
            param = (int(p_id),str(r_id) ,str(r_name),str(r_location),int(r_followers_count),int(r_listed_count),str(r_favourites_count),int(r_statuses_count),str(r_profile_image_url_https))
            #execute the sql query
            cursor.execute(sql,param)
            # commit the changes
            cnxn.commit()
            
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred in INSERT to PAGES - insert_pages. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method insert_pages

# Method to truncate records from the file PAGES
def truncate_pages():

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #Truncate query for PAGES
            sql = '''TRUNCATE TABLE PAGES'''
            cursor.execute(sql)
            cnxn.commit()
                        
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred in TRUNCATE to PAGES - truncate_pages. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method truncate_pages

# Method to select records from the file PAGES            
def select_pages():

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #Select query for PAGES
            sql = '''SELECT P_ID,FOLLOWERS_COUNT,LISTED_COUNT,FAV_COUNT,STATUSES_COUNT,NAME FROM PAGES ORDER BY P_ID DESC'''
            cursor.execute(sql)
            result=cursor.fetchall()
            return (result)
                        
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred in SELECT to PAGES. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method select_pages

# Method to select records from the file PAGES_TWEET
def truncate_pages_tweet():

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            cursor.execute("TRUNCATE TABLE PAGES_TWEET")
            cnxn.commit()
                        
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred in TRUNCATE to PAGES_TWEET. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method truncate_pages_tweet

# Method to select records from the file PAGES    
def select_pages_url(c):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #Insert query for TWEET_STREAM
            sql = '''SELECT NAME,LOCATION,FOLLOWERS_COUNT,LISTED_COUNT,FAV_COUNT,STATUSES_COUNT,PROFILE_IMAGE_URL_HTTPS FROM PAGES'''
            cursor.execute(sql)
            result=cursor.fetchall()
            return (result[c-1])
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred on SELECT query on PAGES - select_pages_url. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method select_pages_url

# Method to select records from the file PAGES_TWEET 
def insert_pages_tweet(p_id,r_id,r_text,r_created_at,r_favorite_count,r_retweet_count):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            sql = '''INSERT INTO PAGES_TWEET (P_ID,ID, TWEET, CREATED_AT, FAV_COUNT,RETWEET_COUNT) VALUES (?,?,?,?,?,?)'''
            parm = (int(p_id),int(r_id),str(r_text),str(r_created_at),int(r_favorite_count),int(r_retweet_count))
            cursor.execute(sql,parm)
            cnxn.commit()
                        
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred in INSERT to PAGES_TWEET - insert_pages_tweet. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method insert_pages_tweet

# Method to select records from the file PAGES_TWEET 
def select_pages_tweet():

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #Insert query for TWEET_STREAM
            sql = '''SELECT PAGE_TWEEET_ID, FAV_COUNT,RETWEET_COUNT ,P_ID FROM PAGES_TWEET ORDER BY PAGE_TWEEET_ID '''
            cursor.execute(sql)
            result=cursor.fetchall()
            return (result)
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred on SELECT query on PAGES_TWEET - select_pages_tweet. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method select_pages_tweet

# Method to truncate records from the file PAGES_REPLY
def truncate_pages_reply():

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #Truncate query for PAGES_REPLY
            sql = '''TRUNCATE TABLE PAGES_REPLY'''
            cursor.execute(sql)
            cnxn.commit()
                        
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred in TRUNCATE to PAGES_REPLY - truncate_pages_reply. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method truncate_pages_reply

# Method to select records from the file PAGES_REPLY 
def insert_pages_reply(p_id,r_text,r_in_reply_to_status_id_str,r_reply_text,r_polarity):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            sql = '''INSERT INTO PAGES_REPLY (P_ID, TWEET, IN_REPLY_TO_STATUS_ID, REPLY_TEXT,POLARITY) VALUES (?,?,?,?,?)'''
            parm = (int(p_id),str(r_text),int(r_in_reply_to_status_id_str),str(r_reply_text),float(r_polarity))
            cursor.execute(sql,parm)
            cnxn.commit()
                        
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred in INSERT to PAGES_REPLY - insert_pages_reply. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method insert_stream

# Method to select records from the file PAGES_REPLY 
def select_reply(r_in_reply_to_status_id_str):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #Select query for TWEET_STREAM
            sql = '''SELECT POLARITY FROM PAGES_REPLY WHERE IN_REPLY_TO_STATUS_ID = ? '''
            param = (str(r_in_reply_to_status_id_str))
            cursor.execute(sql,param)
            result=cursor.fetchall()
            return (result)
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred on SELECT query on PAGES_REPLY. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method select_search

# Method to select records from the file PAGES_REPLY 
def count_reply(r_in_reply_to_status_id_str):

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            #Insert query for TWEET_STREAM
            sql = '''SELECT COUNT(IN_REPLY_TO_STATUS_ID) FROM PAGES_REPLY WHERE IN_REPLY_TO_STATUS_ID=? GROUP BY IN_REPLY_TO_STATUS_ID;'''
            param = (str(r_in_reply_to_status_id_str))
            cursor.execute(sql,param)
            result=cursor.fetchall()
            return (result)
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred on SELECT query on PAGES_REPLY - count_reply. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method count_reply

# Method to select records from the file PAGES 
def select_pages_table():

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            sql = '''SELECT FOLLOWERS_COUNT,LISTED_COUNT,FAV_COUNT,STATUSES_COUNT FROM PAGES'''
            cursor.execute(sql)
            result=cursor.fetchall()
            return (result)
                        
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred in SELECT to PAGES - select_pages_table. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method select_pages_table

# Method to select records from the file PAGES 
def select_pages_name():

    #establish connection
    cnxn = connection ()

    #execeute only if connection is established
    if cnxn is not None:
        try:
            cursor = cnxn.cursor()
            sql = '''SELECT NAME FROM PAGES'''
            cursor.execute(sql)
            result=cursor.fetchall()
            return (result)
                        
        except Exception as e:
            # rollback on error
            cnxn.rollback()
            #display error message
            print ("Error occurred in SELECT to PAGES - select_pages_name. Rolback sucessful! \nThis record is skipped and processing will continue\n",e)
            #tkinter.messagebox.showinfo("An Error occured : ",e)

    cnxn.close()
#end of method select_pages_name
