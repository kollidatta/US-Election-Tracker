# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 16:19:49 2020

@author: prabhakar reddy
"""


#GetOldTweets module helps us to scrap the twitter based on the key word or the 
#user details
import GetOldTweets3 as got
import pandas as pd
import regex as re
from datetime import date as dt
import sqlite3
from sqlalchemy import create_engine
from statistics import mean


engine = create_engine('sqlite://', echo=False)

#creating the empty lists to collect the data
trump = []
biden = []
t_date = []
tweet = []  

#This Function gets the tweets from the twitter page
def twitter_scrapper(name):
    username = name
    count = 10
    # Creation of query object
    tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
                                            .setMaxTweets(count)
    # Creation of list that contains all tweets
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    # Creating list of chosen tweet data
    user_tweets = [[tweet.date, tweet.text] for tweet in tweets]
    tweet_date = [[tweet.date] for tweet in tweets]
       
    return user_tweets

# def data_Checker(tweetdate):
#     for date in tweetdate:
#         print(date)                  

def val_appender(user_tweets, page, words):
     
    #test_words = ['National GE','Trump','Biden']
    test_words = words
    for tweets in user_tweets:
        #Checks the test_w0rds in the tweet
        if all(x in str(tweets) for x in test_words):
            
                        
            #appends the data and tweet for future reference
            dat = tweets[0].now().date()
            print(dat)
            #checks for todays tweet
            if dat == dt.today():
                t_date.append(dat)
            
                tweet.append(tweets[1])           
                b = str(tweets).split(' ')
            
                for i in range(0, len(b)):
                    if b[i] =='Trump':
                        temp = b[i+1][:2]
                        #checks the selected string as digit and saves them 
                        if temp.isdigit() ==True:
                            trump.append(temp)
                        
                    elif b[i]=='Biden':
                        temp = b[i+1][:2]
                        #checks the selected string as digit and saves them 
                        if temp.isdigit() ==True:
                            biden.append(temp)
    
    return t_date, trump, biden

def date_seg(df, df1):
        
    
    foo = lambda a:round( mean(a) )
    df2 = df.groupby(by='Date').agg({foo}).reset_index()   
    
    foo = lambda a:round( mean(a) )
    df3 = df1.groupby(by='Date').agg({foo}).reset_index()
        

        
if __name__ =="__main__":
        
    #Selected Twitter users and testwords
    users = ['PpollingNumbers','Politics_Polls']
    test_words = [['National Poll','Trump','Biden'], ['National GE','Trump','Biden']]
    
       
    for i in range(0,len(users)):
        tweets = twitter_scrapper(users[i]) 
        date, trump, biden = val_appender(tweets, users[i], test_words[i])
    
    
   
    #creating the dataframe from the lists created    
    grp = pd.DataFrame(list(zip(date,trump, biden)), columns=['Date', 'Trump', 'Biden' ])        
    #grp['Date'] = grp['Date'].dt.date
    
    
    df = grp[['Date', 'Trump']].copy()
    df['Trump'] = pd.to_numeric(df['Trump'])
   
    df1 =  grp[['Date', 'Biden']].copy() 
    df1['Biden'] = pd.to_numeric(df1['Biden'])
    
    grp_df = date_seg(df, df1)
    
    #saving df into SQL         
    grp.to_sql('Polling', con=engine, if_exists='replace')
    engine.execute("SELECT * FROM Polling").fetchall() 

           

    