''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Created by      : Gowrisankar & Ashok
Created at      : April 10, 2018
Module name     : UI.py
Description     : This module contains all the GUI screen and makes the necessary calls to the other
                  modules for essential functions like reading the tweets from twitter plotting the
                  graph, storing the read tweets into the database
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import DB_Operations
import webbrowser
from PIL import ImageTk, Image
from io import BytesIO
import scatterplot
import trend
import sentiment
import wordclod
import treemap
import hashlib
import Tweet
import search
import sys
import os
import image
import users
import posttweet
import page_tweets
import in_sentiment
import comparison






#Function to perform username and password validation
def login():
    if username.get()!="" and passvar.get()!="" :
        dbname,dbpass=DB_Operations.uservalid(username.get(),passvar.get())
        hashpass=hashlib.md5(passvar.get().encode())
        h=hashpass.hexdigest()
        if dbname==username.get() and dbpass==h :
            screenone.root.destroy()
            screenthree()
        else:
            messagebox.showinfo("Login- Failed", "Username-Password pair does not exist")
            passvar.set('')
            username.set('')
    else:
        messagebox.showinfo("Login- Failed", "Fields Empty")
        
#Function to perform user sign up        
def signup():
    if finame.get()=="" or laname.get()=="" or uname.get()=="" or pass1.get()=="" or pwd.get()=="" :
        messagebox.showinfo("SignUp", "One/More fields missing")
    elif finame.get().isalpha() and laname.get().isalpha():
        if pwd.get()== pass1.get():
            c=DB_Operations.sigup(finame.get(),laname.get(),uname.get(),pwd.get())
            if c==1:
                messagebox.showinfo("SignUp", "SignUp sucessfull, Going Back to Login screen")
                screentwo.root.destroy()
                screenone()
            elif c==0:
                messagebox.showinfo("SignUp", "Username not available, already taken")
                uname.set('')
                pwd.set("")
                pass1.set("") 
        else:
            messagebox.showinfo("SignUp", "Password do not match")
            pwd.set("")
            pass1.set("") 
    else:
        messagebox.showinfo("SignUp", "First and Last name should contain only alphabets")
        laname.set("");finame.set("")
        
#Function to confirm user decision of logging out 
def logout():
    answer=messagebox.askokcancel("Logout","Are you sure to Log out?")
    if answer:
        screenthree.root.destroy()
        screenone()
        
#Function to confirm user selection to exit application
def exit():
    answer=messagebox.askokcancel("Exit","Application will be closed")
    if answer:
        screenone.root.destroy()
        print("pixel-tweets by Gowrisankar Arumugan, Ashok Ramasami")
        sys.exit()

#Function to pull the top5 trending topics in twitter and return it to the listbox
def trending():
    screenthree.root.destroy()
    t=Tweet.trending()
    screenfour(t)
    
#Function to send the selection of the trending term chose and count to read the no.of.tweets in streaming api
def plots(a,t,count):
    a=str(a).replace(',','').replace('(','').replace(')','')
    if a!=""and count!="" and count.isnumeric():
        a=int(a)
        plots.d=t[a]
        if os.path.exists('./TXT/streamcloud.txt'):
           os.remove('./TXT/streamcloud.txt')
        dupe()
        plots.sid=Tweet.main(t[a],int(count))
    else:
        messagebox.showinfo("Error", "Invalid selection!")
        
#Function to send the user choice input of tweet topic and the no of tweet to be analysed
def searching():
    if count.get()!="" and searchterm.get()!="" and  count.get().isnumeric():
        
        searching.id=search.main(searchterm.get(),int(count.get()))
        dupe1()
    else:
        messagebox.showinfo("Error", "Invalid choice")
        
#Function to display the charting buttons once the tweets are inserted into the database
def dupe():
        screenfour.btn3.pack(padx=10, pady=10,side=LEFT);screenfour.btn4.pack(padx=10, pady=10,side=LEFT)
        screenfour.btn5.pack(padx=10, pady=10,side=LEFT);screenfour.btn6.pack(padx=10, pady=10,side=LEFT)

#Function to display the charting buttons once the tweets are inserted into the database        
def dupe1():
        screenfive.btn3.pack(padx=10, pady=10,side=LEFT);screenfive.btn4.pack(padx=10, pady=10,side=LEFT)
        screenfive.btn5.pack(padx=10, pady=10,side=LEFT);screenfive.btn6.pack(padx=10, pady=10,side=LEFT)
        
#Function to hide the buttons and clear selection once the fields are reset
def reset():
        hidesearch()
        searchterm.set("")
        count.set("")
        
#Function to hide the buttons and clear selection once the fields are reset        
def rest():
    hidestream()
    cnt.set("")
    screenfour.listbox.select_clear(0,END)
    
#Function to hide the buttons
def hidestream():
    screenfour.btn3.pack_forget();screenfour.btn4.pack_forget();
    screenfour.btn5.pack_forget();screenfour.btn6.pack_forget();

#Function to hide the buttons
def hidesearch():
        screenfive.btn3.pack_forget();screenfive.btn4.pack_forget();
        screenfive.btn5.pack_forget();screenfive.btn6.pack_forget();

#Function to call the module to plot the polarity vs time of search in a trend plot
def pol(a,t):
    a=str(a).replace(',','').replace('(','').replace(')','')
    if a!="":
        a=int(a)
        trend.graph(int(t[a][0]),t[a][1])
    else:
        messagebox.showinfo("Error", "No selection made!")
        
#Funtion to open the official twitter handle through binding the event to a tkinter message     
def callback(event):
    link=image.linking()
    webbrowser.open_new(r"%s"%link)

#Function to call the module to post the tweet in the user twitter handle
def post():
    if new.get()=="":
        messagebox.showinfo("Error", "Cannot tweet empty post")
    else:
        posttweet.main(new.get())
        new.set("")

#The Tkinter window that displays details about the user twitter handle like followers, handle name etc   
def screeneight(c):
        global new
        screeneight.root = tk.Tk()
        screeneight.root.title('pixel_tweets')
        s_width=screeneight.root.winfo_screenwidth()
        s_height=screeneight.root.winfo_screenheight()
        xco=(s_width/2)-(450/2)
        yco=(s_height/2)-(300/2)
        screeneight.root.geometry('450x300+%d+%d'%(xco,yco))

        raw_data,follower,lis,fav,status,name=image.main(c)

        frame1 = Frame(screeneight.root)       # add a row of buttons
        frame1.pack()

        im = Image.open(BytesIO(raw_data))
        photo = ImageTk.PhotoImage(im)
        label = tk.Label(frame1,image=photo)
        label.image = photo
        label.grid(row=1, column=0, rowspan=3,sticky=W+E+N+S)
        name= Label(frame1, text='%s'%name,width=10)
        name.grid(row=3, column=0,pady=(10,0), sticky=W)        
        
        Tweets= Label(frame1, text='Tweets',width=10)
        Tweets.grid(row=1, column=1,padx=(10, 0),pady=(10,0), sticky=W)
        Followers= Label(frame1, text='Followers',width=10)
        Followers.grid(row=1, column=2,pady=(10,0), sticky=W)
        Likes= Label(frame1, text='Likes',width=10)
        Likes.grid(row=1, column=3,pady=(10,0), sticky=W)
        List= Label(frame1, text='List',width=10)
        List.grid(row=1, column=4,pady=(10,0), sticky=W)        
        T= Label(frame1, text='%s'%status,width=10)
        T.grid(row=2, column=1,padx=(10, 0), sticky=W)
        F= Label(frame1, text='%s'%follower,width=10)
        F.grid(row=2, column=2, sticky=W)
        L= Label(frame1, text='%s'%fav,width=10)
        L.grid(row=2, column=3, sticky=W)
        LA= Label(frame1, text='%s'%lis,width=10)
        LA.grid(row=2, column=4, sticky=W)

        link = Label(frame1, text=" Official Twitter Handle", fg="blue")
        link.grid(row=3, column=2,columnspan=5,padx=(10, 0), sticky=W)
        link.bind("<Button-1>", callback)
        
        
        frame1 = Frame(screeneight.root)       # add a row of buttons
        frame1.pack()
        dum=Label(frame1, text=" New Tweet:")
        dum.pack_forget()
        new = StringVar()
        twy = Entry(frame1, textvariable=new,width=30)
        twy.pack_forget()
        btn5 = Button(frame1,text=" Post ",width=10,command=post)
        
        frame1 = Frame(screeneight.root)       # add a row of buttons
        frame1.pack()
        screeneight.btn1 = Button(frame1,text=" Comparison ",width=20,command=lambda:(comparison.main(c)))
        screeneight.btn2 = Button(frame1,text=" Latest 25 tweets ",width=20,command=lambda:(page_tweets.main(c)))
        screeneight.btn3 = Button(frame1,text=" Latest tweet sentiment ",width=20,command=lambda:(in_sentiment.useful(c)))
        btn4 = Button(frame1,text=" Back ",width=10,command=lambda:(screeneight.root.destroy(),screenseven() if c!=6 else screenthree()))
        screeneight.btn1.pack(padx=10, pady=10);screeneight.btn2.pack(padx=10, pady=10);
        screeneight.btn3.pack(padx=10, pady=10);btn4.pack(padx=10, pady=10)

        if c==6:
            dum.grid(row=0, column=0, sticky=W,pady=10)
            twy.grid(row=0, column=1, sticky=W,pady=10)
            btn5.grid(row=0, column=2, sticky=W,padx=7,pady=10)
            screeneight.btn1.pack_forget()
            
#Tkinter window displays the top tech companies for which the user can ge the details 
def screenseven():
        screenseven.root = Tk()
        screenseven.root.title('pixel_tweets')
        s_width=screenseven.root.winfo_screenwidth()
        s_height=screenseven.root.winfo_screenheight()
        xco=(s_width/2)-(350/2)
        yco=(s_height/2)-(350/2)
        screenseven.root.geometry('350x350+%d+%d'%(xco,yco))

        frame1 = Frame(screenseven.root)       # add a row of buttons
        frame1.pack(side=TOP)
        screenseven.w = Message(master=None, text="Select one to Analyze", width=400)
        screenseven.w.pack(padx=10, pady=10)
        
        frame1 = Frame(screenseven.root)       # add a row of buttons
        frame1.pack()
        
        screenseven.btn1 = Button(frame1,text=" Microsoft ",width=10,command=lambda:(screenseven.root.destroy(),screeneight(1)))
        screenseven.btn2 = Button(frame1,text=" Google ",width=10,command=lambda:(screenseven.root.destroy(),screeneight(2)))
        screenseven.btn3 = Button(frame1,text=" Twitter ",width=10,command=lambda:(screenseven.root.destroy(),screeneight(3)))
        screenseven.btn4 = Button(frame1,text=" IBM ",width=10,command=lambda:(screenseven.root.destroy(),screeneight(4)))
        screenseven.btn5 = Button(frame1,text=" IIT Chicago ",width=10,command=lambda:(screenseven.root.destroy(),screeneight(5)))
        screenseven.btn6 = Button(frame1,text=" Back ",width=7,command=lambda:(screenseven.root.destroy(),screenthree()))
        screenseven.btn1.pack(padx=10, pady=10);screenseven.btn2.pack(padx=10, pady=10);
        screenseven.btn3.pack(padx=10, pady=10);screenseven.btn4.pack(padx=10, pady=10);
        screenseven.btn5.pack(padx=10, pady=10);screenseven.btn6.pack(padx=10, pady=10)

#TKinter window  that tdisplayes the history of the search made by the user so that the trend plot for polarity can be plotted based on the user choice     
def screensix():
        screensix.root = Tk()
        screensix.root.title('pixel_tweets')
        s_width=screensix.root.winfo_screenwidth()
        s_height=screensix.root.winfo_screenheight()
        xco=(s_width/2)-(250/2)
        yco=(s_height/2)-(250/2)
        screensix.root.geometry('250x250+%d+%d'%(xco,yco))

        frame1 = Frame(screensix.root)       # add a row of buttons
        frame1.pack(side=TOP)
        w = Message(master=None, text="List of terms you searched ", width=400)
        w.pack(padx=10, pady=10,side=TOP)
        
        frame1 = Frame(screensix.root)       # allow for selection of names
        frame1.pack()
        scroll = Scrollbar(frame1, orient=VERTICAL)
        screensix.listbox = Listbox(frame1, yscrollcommand=scroll.set, height=8,width=20)
        scroll.config (command=screensix.listbox.yview)
        scroll.pack(side=RIGHT, fill=Y)
        screensix.listbox.pack(side=LEFT,  fill=BOTH)
        t=DB_Operations.getsearchterms()

        for i in range (0,len( t)):
            screensix.listbox.insert(END, t[i][1])
            
        frame1 = Frame(screensix.root)       # add a row of buttons
        frame1.pack()
        btn1 = Button(frame1,text=" Back ",width=7,command=lambda:(screensix.root.destroy(),screenthree()))
        btn2 = Button(frame1,text=" Trend ",width=7,command=lambda:(pol(screensix.listbox.curselection(),t)))
        btn1.pack(padx=10, pady=10,side=LEFT); btn2.pack(padx=10, pady=10,side=LEFT)
        
    
#Tkinter window to get the user inout for the search term and the count of tweets to analyse for user choice    
def screenfive():
    global count,searchterm
    screenfive.root = Tk()
    screenfive.root.title('pixel_tweets')
    s_width=screenfive.root.winfo_screenwidth()
    s_height=screenfive.root.winfo_screenheight()
    xco=(s_width/2)-(450/2)
    yco=(s_height/2)-(250/2)
    screenfive.root.geometry('450x250+%d+%d'%(xco,yco))

    frame1 = Frame(screenfive.root)       # add a row of buttons
    frame1.pack(side=TOP)
    w = Message(master=None, text="Enter the search term", width=400)
    w.pack(padx=10, pady=10,side=TOP)
    
    frame1 = Frame(screenfive.root)
    frame1.pack()

    Label(frame1, text="Search Term:").grid(row=0, column=0, sticky=W,pady=10)
    searchterm = StringVar()
    st = Entry(frame1, textvariable=searchterm)
    st.grid(row=0, column=1, sticky=W,pady=10)

    Label(frame1, text="No.Of tweet:").grid(row=1, column=0, sticky=W,pady=10)
    count= StringVar()
    ct= Entry(frame1, textvariable=count)
    ct.grid(row=1, column=1, sticky=W,pady=10)

    clear = Button(frame1,text=" Reset  ",width=10,command=reset)
    clear.grid(row=0, column=3,padx=5, sticky=W,pady=10)
    
    frame1 = Frame(screenfive.root)       # add a row of buttons
    frame1.pack()
    btn1 = Button(frame1,text=" Analyse  ",width=10,command=lambda:(hidesearch(),searching()))
    btn2 = Button(frame1,text=" Back ",width=10,command=lambda:(screenfive.root.destroy(),screenthree()))
    btn1.pack(padx=10, pady=10,side=RIGHT); btn2.pack(padx=10, pady=10,side=RIGHT)

    frame1 = Frame(screenfive.root)       # add a row of buttons
    frame1.pack()
    screenfive.btn3 = Button(frame1,text=" Sentiment ",width=10,command=lambda:(sentiment.main(searching.id,searchterm.get())))
    screenfive.btn4 = Button(frame1,text=" Wordcloud ",width=10,command=lambda:(wordclod.cloud(searchterm.get(),2,searching.id)))
    screenfive.btn5 = Button(frame1,text=" Device ",width=10,command=lambda:(treemap.main(searchterm.get(),searching.id)))
    screenfive.btn6 = Button(frame1,text=" tweet Reach ",width=10,command=lambda:(scatterplot.main(searchterm.get(),searching.id)))
    screenfive.btn3.pack_forget();screenfive.btn4.pack_forget();
    screenfive.btn5.pack_forget();screenfive.btn6.pack_forget()

#Tkinter window displays the top trending topic in twitter and asks for the no of tweets from the user to analyse for the selected topic    
def screenfour(t):
    global cnt
    screenfour.root = Tk()
    screenfour.root.title('pixel_tweets')
    s_width=screenfour.root.winfo_screenwidth()
    s_height=screenfour.root.winfo_screenheight()
    xco=(s_width/2)-(450/2)
    yco=(s_height/2)-(300/2)
    screenfour.root.geometry('450x300+%d+%d'%(xco,yco))
    frame1 = Frame(screenfour.root)       # add a row of buttons
    frame1.pack()
    header = Message(master=None, text="Select one from the Top 5 trending below", width=350)
    header.pack()     
    screenfour.listbox = Listbox(screenfour.root,height=7)
    screenfour.listbox.pack(pady=10)

    for item in t:
        screenfour.listbox.insert(END, item)

    Label(frame1, text="No.of Tweets").pack( pady=10,side = LEFT )
    cnt=StringVar()
    tc = Entry(frame1, textvariable=cnt)
    tc.pack( pady=10,side = LEFT )
    reset = Button(frame1,text=" Reset ",width=10,command=rest)
    reset.pack( padx=5,side = LEFT )
    frame1 = Frame(screenfour.root)       # add a row of buttons
    frame1.pack()
    btn1 = Button(frame1,text=" Back ",width=10,command=lambda:(screenfour.root.destroy(),screenthree()))
    btn2 = Button(frame1,text=" Analyze ",width=10,command=lambda:(hidestream(),plots(screenfour.listbox.curselection(),t,cnt.get())))
    btn1.pack(padx=10, pady=10,side=LEFT); btn2.pack(padx=10, pady=10,side=LEFT)

    frame1 = Frame(screenfour.root)       # add a row of buttons
    frame1.pack()
    screenfour.btn3 = Button(frame1,text=" Sentiment ",width=10,command=lambda:(sentiment.main(plots.sid,plots.d)))
    screenfour.btn4 = Button(frame1,text=" Wordcloud ",width=10,command=lambda:(wordclod.cloud(plots.d,1,plots.sid)))
    screenfour.btn5 = Button(frame1,text=" Device ",width=10,command=lambda:(treemap.main(plots.d,plots.sid)))
    screenfour.btn6 = Button(frame1,text=" tweet Reach ",width=10,command=lambda:(scatterplot.main(plots.d,plots.sid)))
    screenfour.btn3.pack_forget();screenfour.btn4.pack_forget();
    screenfour.btn5.pack_forget();screenfour.btn6.pack_forget();
    


#Tkinter window displays the home screen of the application from which the user can navigate to other screens
def screenthree () :
    screenthree.root = Tk()
    screenthree.root.title('pixel_tweets')
    s_width=screenthree.root.winfo_screenwidth()
    s_height=screenthree.root.winfo_screenheight()
    xco=(s_width/2)-(350/2)
    yco=(s_height/2)-(350/2)
    screenthree.root.geometry('350x350+%d+%d'%(xco,yco))

    frame1 = Frame(screenthree.root)       # add a row of buttons
    frame1.pack(side=TOP)
    
    header = Message(master=None, text="Hi %s"%(username.get()), width=400)
    header.pack(padx=10, pady=5,side=TOP)
    w = Message(master=None, text="Welcome to Pixel tweet analyzer", width=400)
    w.pack(padx=10, pady=5,side=TOP)

    frame1 = Frame(screenthree.root)       # add a row of buttons
    frame1.pack(side=TOP)
    btn1 = Button(frame1,text=" Top Trending ",width=15,command=trending)
    btn2 = Button(frame1,text=" Search tweets ",width=15,command=lambda:(screenthree.root.destroy(),screenfive()))
    btn3 = Button(frame1,text=" Tech Giant ",width=15,command=lambda:(screenthree.root.destroy(),users.main(),screenseven()))
    btn4 = Button(frame1,text=" History ",width=15,command=lambda:(screenthree.root.destroy(),screensix()))
    btn5 = Button(frame1,text=" My Handle ",width=15,command=lambda:(screenthree.root.destroy(),users.main(),screeneight(6)))
    btn6 = Button(frame1,text=" Logout ",width=10,command=logout)
    btn1.pack(padx=10, pady=10);btn2.pack(padx=10, pady=10);
    btn3.pack(padx=10, pady=10);btn4.pack(padx=10, pady=10);
    btn5.pack(padx=10, pady=10);btn6.pack(padx=10, pady=10);
    
#Tkinter window for user sign up!   
def screentwo():
    screenone.root.destroy()
    global finame,laname,pass1,pwd,uname
    screentwo.root = Tk()
    screentwo.root.title('pixel_tweets')
    s_width=screentwo.root.winfo_screenwidth()
    s_height=screentwo.root.winfo_screenheight()
    xco=(s_width/2)-(350/2)
    yco=(s_height/2)-(350/2)
    screentwo.root.geometry('350x350+%d+%d'%(xco,yco))

    frame1 = Frame(screentwo.root)       # add a row of buttons
    frame1.pack(side=TOP)
    w = Message(master=None, text="Registration", width=400)
    w.pack(padx=10, pady=10,side=TOP)

    frame1 = Frame(screentwo.root)
    frame1.pack()

    Label(frame1, text="First Name").grid(row=0, column=0, sticky=W,pady=10)
    finame = StringVar()
    fname = Entry(frame1, textvariable=finame)
    fname.grid(row=0, column=1, sticky=W,pady=10)

    Label(frame1, text="Last Name").grid(row=3, column=0, sticky=W,pady=10)
    laname = StringVar()
    lname = Entry(frame1, textvariable=laname)
    lname.grid(row=3, column=1, sticky=W,pady=10)

    Label(frame1, text="Username").grid(row=5, column=0, sticky=W,pady=10)
    uname=StringVar()
    name = Entry(frame1, textvariable=uname)
    name.grid(row=5, column=1, sticky=W,pady=10)

    Label(frame1, text="Password").grid(row=7, column=0, sticky=W)
    pwd=StringVar()
    password = Entry(frame1,show='*', textvariable=pwd)
    password.grid(row=7, column=1, sticky=W,pady=10)

    Label(frame1, text="Re-Type Password").grid(row=9,column=0, sticky=W,pady=10)
    pass1 = StringVar()
    password1 = Entry(frame1,show='*', textvariable=pass1)
    password1.grid(row=9, column=1, sticky=W,pady=10)

    frame1 = Frame(screentwo.root)       # add a row of buttons
    frame1.pack()
    btn1 = Button(frame1,text=" Register  ",width=10,command=signup)
    btn2 = Button(frame1,text=" Back ",width=10,command=lambda:(screentwo.root.destroy(),screenone()))
    btn1.pack(padx=10, pady=10,side=RIGHT); btn2.pack(padx=10, pady=10,side=RIGHT)


#TKinter window for signing in to the application 
def screenone () :             #Application interface 
    global username, passvar
    screenone.root = Tk()
    screenone.root.title('pixel_tweets')
    s_width=screenone.root.winfo_screenwidth()
    s_height=screenone.root.winfo_screenheight()
    xco=(s_width/2)-(250/2)
    yco=(s_height/2)-(180/2)
    screenone.root.geometry('250x180+%d+%d'%(xco,yco))
    
    frame1 = Frame(screenone.root)       # add a row of buttons
    frame1.pack(side=TOP)
    w = Message(master=None, text="Welcome to pixel_tweets tweet analyzer", width=400)
    w.pack(padx=10, pady=10,side=TOP)
    
    frame1 = Frame(screenone.root)
    frame1.pack()

    Label(frame1, text="Username:").grid(row=0, column=0, sticky=W,pady=10)
    username = StringVar()
    name = Entry(frame1, textvariable=username)
    name.grid(row=0, column=1, sticky=W,pady=10)

    Label(frame1, text="Password:").grid(row=1, column=0, sticky=W,pady=10)
    passvar= StringVar()
    password= Entry(frame1,show='*', textvariable=passvar)
    password.grid(row=1, column=1, sticky=W,pady=10)
	
    
    frame1 = Frame(screenone.root)       # add a row of buttons
    frame1.pack()
    btn1 = Button(frame1,text=" Login  ",width=7,command=login)
    btn2 = Button(frame1,text=" Sign Up!",width=7,command=screentwo)
    btn3 = Button(frame1,text=" Exit ",width=7,command=exit)
    btn1.pack(padx=10, pady=10,side=RIGHT); btn2.pack(padx=10, pady=10,side=RIGHT)
    btn3.pack(pady=10, padx=10, side=RIGHT);         
    return screenone.root

screenone()

